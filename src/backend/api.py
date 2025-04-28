from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from stable_baselines3 import PPO
from src.enforcement_learning.traffic_env import TrafficEnv
from fastapi.staticfiles import StaticFiles
from src.vision.annotator import annotate_vehicles
from src.vision.detector import capture_frame, count_vehicles_from_frame
from src.vision.annotator import annotate_frame

frame_counter = 0
SKIP_FRAMES = 5  # Adjustable


app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
annotate_vehicles("data/raw/sample.png", "static/output.jpg")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

env = TrafficEnv()
model = PPO.load("models/ppo_traffic_signal.zip")

@app.get("/step")
def step():
    frame = capture_frame()
    vehicle_counts, results = count_vehicles_from_frame(frame)
    annotate_frame(frame, results, "static/output.jpg")
    env.set_state(vehicle_counts)  # Add this method to your TrafficEnv if not already there
    action, _ = model.predict(vehicle_counts)
    new_state, reward, done, _, _ = env.step(action)

    return {
        "state": vehicle_counts,
        "action": int(action),
        "action_label": {0: "Green (NS)", 1: "Green (EW)", 2: "All Red"}[int(action)],
        "reward": float(reward),
        "image_url": "/static/output.jpg"
    }
