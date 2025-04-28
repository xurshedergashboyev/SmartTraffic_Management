# src/prediction/lstm_predictor.py
import numpy as np
from tensorflow.keras.models import load_model
from sklearn.preprocessing import MinMaxScaler

model = load_model("models/lstm_traffic_predictor.h5")

scaler = MinMaxScaler()
scaler.min_, scaler.scale_ = np.array([0.0]), np.array([1.0])  # adjust if you saved the real ones

SEQ_LEN = 10

def predict_next_count(history: list[int]) -> int:
    data = np.array(history).reshape(-1, 1)
    data_scaled = scaler.transform(data)
    X = np.expand_dims(data_scaled[-SEQ_LEN:], axis=0)
    pred_scaled = model.predict(X)
    pred = scaler.inverse_transform(pred_scaled)
    return int(pred[0][0])
