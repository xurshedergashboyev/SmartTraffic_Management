import gymnasium as gym
import numpy as np

class TrafficEnv(gym.Env):
    def __init__(self):
        super(TrafficEnv, self).__init__()

        # 3 possible actions:
        # 0 = Green N-S (lane 0), 1 = Green E-W (lane 1), 2 = All Red
        self.action_space = gym.spaces.Discrete(3)

        # Observation: [vehicles_lane_0, vehicles_lane_1]
        self.observation_space = gym.spaces.Box(low=0, high=100, shape=(2,), dtype=np.int32)

        self.state = None
        self.last_action = 0
        self.time_step = 0

    # In TrafficEnv class
    def set_state(self, new_state):
        self.state = np.array(new_state)

    def reset(self, seed=None):
        super().reset(seed=seed)
        self.state = np.random.randint(0, 10, size=(2,))
        self.last_action = 0
        self.time_step = 0
        return self.state, {}

    def step(self, action):
        self.time_step += 1
        done = False

        # Simulate vehicle flow
        if action == 0:  # Green for N-S (lane 0)
            self.state[0] = max(0, self.state[0] - np.random.randint(4, 8))
            self.state[1] += np.random.randint(1, 4)
        elif action == 1:  # Green for E-W (lane 1)
            self.state[1] = max(0, self.state[1] - np.random.randint(4, 8))
            self.state[0] += np.random.randint(1, 4)
        else:  # All red
            self.state += np.random.randint(1, 3, size=(2,))

        # Reward: negative total wait + penalty for switching signals
        penalty = -2 if action != self.last_action else 0
        reward = -np.sum(self.state) + penalty

        self.last_action = action

        # End simulation after 50 steps
        if self.time_step >= 50:
            done = True

        return self.state, reward, done, False, {}

    def render(self):
        print(f"Traffic State: {self.state}")
