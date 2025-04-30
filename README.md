# SmartTraffic Dashboard

A full-stack traffic simulation dashboard that integrates computer vision and time series forecasting to optimize real-time traffic signals. The project leverages YOLO object detection for live car counting and an LSTM model for predictive signal control.

## Overview

This system simulates a smart intersection where traffic lights are controlled based on live input and predictive analytics. The goal is to optimize throughput and reduce congestion using:

- **YOLOv5** for vehicle detection on simulated video frames.
- **LSTM** model for predicting traffic volume trends.
- **FastAPI** backend serving frame data, state updates, and reward information.
- **React/TypeScript** frontend dashboard to visualize state, actions, rewards, and predictions.

## Setup Instructions

### 1. Backend (FastAPI + YOLO + LSTM)

#### Python Environment
```bash
cd backend
python -m venv venv
source venv/bin/activate
```

#### Run FastAPI
```bash
uvicorn api:app --reload
```
This starts the API server at `http://localhost:8000`.

Make sure your YOLO model weights are downloaded and accessible, and your LSTM model is saved/trained in the correct location.

---

### 2. Frontend (React + TypeScript)

#### Install Dependencies
```bash
cd dashboard
npm install
```

#### ▶Start the Dashboard
```bash
npm run dev
```
The dashboard runs at `http://localhost:5173` (or similar).

## Dashboard Features

- Real-time traffic queue visualization
- Signal status and action feedback
- LSTM forecast chart
- Per-step reward tracking
- “Step” and “Run” controls for advancing the simulation

---

## Dependencies

### Backend:
- `fastapi`
- `uvicorn`
- `torch`, `torchvision`
- `opencv-python`
- `pandas`, `numpy`
- `scikit-learn`

### Frontend:
- `react`, `typescript`
- `tailwindcss`
- `recharts` (for visualizations)
- `lucide-react`, `shadcn/ui` (for UI components)

---
