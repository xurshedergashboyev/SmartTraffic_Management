import React, {useState} from "react";
import './index.css';

type StepResponse = {
    state: [number, number];
    action: number;
    action_label: string;
    reward: number;
    image_url: string;
};

const App: React.FC = () => {
    const [data, setData] = useState<StepResponse | null>(null);
    const [error, setError] = useState<string | null>(null);

    const fetchStep = async () => {
        try {
            const res = await fetch("http://127.0.0.1:8000/step");
            if (!res.ok) throw new Error("Failed to fetch /step");
            const json = await res.json();
            setData(json);
            setError(null);
        } catch (err: any) {
            setError(err.message);
        }
    };

    return (
        <div className="p-6 font-mono">
            <h1 className="text-2xl font-bold mb-4">Smart Traffic Controller</h1>

            <button
                onClick={fetchStep}
                className="bg-blue-600 text-white px-4 py-2 rounded shadow mb-6 hover:bg-blue-700 transition"
            >
                Step
            </button>

            {error && <p className="text-red-600">Error: {error}</p>}

            {data ? (
                <div className="space-y-4">
                    <div>
                        <p><strong>Detected Vehicles</strong></p>
                        <ul className="list-disc list-inside">
                            <li>Lane 0: {data.state[0]}</li>
                            <li>Lane 1: {data.state[1]}</li>
                        </ul>
                    </div>

                    <div>
                        <p><strong>Current Action</strong>: {data.action_label}</p>
                    </div>

                    <div>
                        <p><strong>Reward</strong>: <span
                            className={data.reward < 0 ? "text-red-600" : "text-green-600"}>
              {data.reward}
            </span></p>
                    </div>

                    <div>
                        <p><strong>Frame</strong></p>
                        <img src={`http://127.0.0.1:8000${data.image_url}`} alt="Traffic Frame" width={800} height={"auto"}
                             className="w-full max-w-md border rounded"/>
                    </div>
                </div>
            ) : (
                <p>Click "Step" to fetch traffic data.</p>
            )}
        </div>
    );
};

export default App;
