from ultralytics import YOLO
import cv2

model = YOLO("yolov8n.pt")

def annotate_vehicles(image_path: str, output_path: str = "output.jpg"):
    image = cv2.imread(image_path)
    if image is None:
        raise FileNotFoundError(f"Image not found at {image_path}")

    results = model(image)[0]
    boxes = results.boxes
    vehicle_classes = [2, 3, 5, 7]  # car, motorcycle, bus, truck

    lane_split = image.shape[1] // 2
    counts = [0, 0]  # lane 0, lane 1

    for box in boxes:
        cls = int(box.cls[0])
        if cls in vehicle_classes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            center_x = int(box.xywh[0][0])
            lane = 0 if center_x < lane_split else 1
            counts[lane] += 1

            color = (0, 255, 0) if lane == 0 else (255, 0, 0)
            label = f"Lane {lane}"
            cv2.rectangle(image, (x1, y1), (x2, y2), color, 2)
            cv2.putText(image, label, (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

    # Draw center split line
    cv2.line(image, (lane_split, 0), (lane_split, image.shape[0]), (0, 0, 255), 2)

    cv2.imwrite(output_path, image)
    print(f"✅ Annotated image saved to: {output_path}")

def annotate_frame(frame, results, output_path):
    lane_split = frame.shape[1] // 2

    for box in results.boxes:
        cls = int(box.cls[0])
        if cls in [2, 3, 5, 7]:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            center_x = int(box.xywh[0][0])
            lane = 0 if center_x < lane_split else 1
            color = (0, 255, 0) if lane == 0 else (255, 0, 0)
            label = f"Lane {lane}"
            cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
            cv2.putText(frame, label, (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

    cv2.line(frame, (lane_split, 0), (lane_split, frame.shape[0]), (0, 0, 255), 2)
    cv2.imwrite(output_path, frame)
