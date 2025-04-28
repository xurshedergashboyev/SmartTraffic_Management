import { useState, useEffect } from "react";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from "recharts";

interface TrafficState {
  state: number[];
  action_label: string;
  step: number;
  reward: number;
  image_url: string;
}

function App() {
  const [traffic, setTraffic] = useState<TrafficState[]>([]);
  const [step, setStep] = useState<number>(0);
  const [autoMode, setAutoMode] = useState<boolean>(false);
  const [skipMode, setSkipMode] = useState<boolean>(true);


  useEffect(() => {
    // @ts-ignore
      let interval: NodeJS.Timeout;
    if (autoMode) {
      interval = setInterval(() => {
        handleStep();
      }, 2000);
    }
    return () => clearInterval(interval);
  }, [autoMode, skipMode]);

  const handleStep = async () => {
    const res = await fetch(
      `http://localhost:8000/step?skip=${skipMode}&every=5`
    );
    const data = await res.json();

    setTraffic((prev) => [
      ...prev,
      {
        state: data.state,
        action_label: data.action_label,
        step: step + 1,
        reward: data.reward,
        image_url: data.image_url,
      },
    ]);

    setStep((s) => s + 1);
  };

  const latest = traffic[traffic.length - 1];

  return (
    <div className="min-h-screen bg-gray-100 p-6">
      <h1 className="text-3xl font-bold mb-4">🚦 Smart Traffic Dashboard</h1>

      {/* --- Controls --- */}
      <div className="mb-6 space-x-2">
        <button
          onClick={handleStep}
          className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
        >
          Step Simulation
        </button>

        <button
          onClick={() => setAutoMode((prev) => !prev)}
          className="bg-purple-600 text-white px-4 py-2 rounded hover:bg-purple-700"
        >
          {autoMode ? "🛑 Stop Auto-Sim" : "▶️ Start Auto-Sim"}
        </button>

        <button
          onClick={() => setSkipMode((prev) => !prev)}
          className="bg-yellow-500 text-white px-4 py-2 rounded hover:bg-yellow-600"
        >
          {skipMode ? "🟢 Skip: ON" : "🔴 Skip: OFF"}
        </button>
      </div>

      {/* --- Latest State --- */}
      <div className="bg-white p-4 rounded shadow mb-6">
        {latest && (
          <>
            <p className="text-lg font-semibold">
              Latest Traffic State: [Lane 0: {latest.state[0]}, Lane 1:{" "}
              {latest.state[1]}]
            </p>
            <div className="mt-2 flex items-center space-x-2">
              <p className="text-md text-gray-700">Last Action:</p>
              <span className="font-semibold">{latest.action_label}</span>
              <div
                className={`w-4 h-4 rounded-full ${
                  latest.action_label === "Green (NS)"
                    ? "bg-green-500"
                    : latest.action_label === "Green (EW)"
                    ? "bg-red-500"
                    : latest.action_label === "All Red"
                    ? "bg-yellow-400"
                    : "bg-gray-400"
                }`}
              />
            </div>
            <p className="text-md text-gray-600 mt-2">
              Reward:{" "}
              <span
                className={`font-bold ${
                  latest.reward > 0
                    ? "text-green-600"
                    : latest.reward < 0
                    ? "text-red-600"
                    : "text-gray-600"
                }`}
              >
                {latest.reward}
              </span>
            </p>
            {latest.action_label === "Skipped" && (
              <p className="text-sm italic text-gray-400">Frame skipped</p>
            )}
          </>
        )}
      </div>

      {/* --- YOLO Image Preview --- */}
      {latest?.image_url && (
        <div className="bg-white p-4 rounded shadow mb-6">
          <h2 className="text-xl font-semibold mb-2">Live YOLO Detection</h2>
          <img
            src={`http://localhost:8000${latest.image_url}?t=${Date.now()}`}
            alt="YOLO Annotated"
            width={800}
            className="rounded border border-gray-300 shadow-md max-w-full"
          />
        </div>
      )}

      {/* --- Traffic Flow Chart --- */}
      <div className="bg-white p-4 rounded shadow">
        <h2 className="text-xl font-semibold mb-4">Traffic Flow History</h2>
        <ResponsiveContainer width="100%" height={300}>
          <LineChart
            data={traffic.map((t) => ({
              step: t.step,
              lane0: t.state[0],
              lane1: t.state[1],
              reward: t.reward,
            }))}
          >
            <XAxis dataKey="step" />
            <YAxis />
            <Tooltip />
            <Legend />
            <Line type="monotone" dataKey="lane0" stroke="#8884d8" name="Lane 0" />
            <Line type="monotone" dataKey="lane1" stroke="#82ca9d" name="Lane 1" />
            <Line
              type="monotone"
              dataKey="reward"
              stroke="#ff7300"
              strokeDasharray="3 3"
              name="Reward"
            />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}

export default App;
