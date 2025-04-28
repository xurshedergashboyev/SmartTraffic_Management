import cv2
from ultralytics import YOLO

model = YOLO("yolov8n.pt")

video_capture = cv2.VideoCapture("data/IMG_3625.mov")

def capture_frame():
    success, frame = video_capture.read()
    if not success:
        raise RuntimeError("Failed to read frame from webcam or video.")
    return frame

def count_vehicles_from_frame(frame):
    results = model(frame)[0]
    boxes = results.boxes
    vehicle_classes = [2, 3, 5, 7]

    lane_split = frame.shape[1] // 2
    counts = [0, 0]

    for box in boxes:
        cls = int(box.cls[0])
        if cls in vehicle_classes:
            center_x = int(box.xywh[0][0])
            lane = 0 if center_x < lane_split else 1
            counts[lane] += 1

    return counts, results
