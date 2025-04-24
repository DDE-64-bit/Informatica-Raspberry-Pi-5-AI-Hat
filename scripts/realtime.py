import cv2
from ultralytics import YOLO
import argparse

try:
    from hailo_sdk_client import Inferencer
    HAILO_AVAILABLE = True
except ImportError:
    HAILO_AVAILABLE = False
    print("Hailo SDK niet gevonden, alleen CPU/GPU modus beschikbaar!")

def find_first_working_camera(max_index=5):
    for i in range(max_index):
        cap = cv2.VideoCapture(i)
        if cap.isOpened():
            cap.release()
            print(f"[INFO] Eerste werkende camera gevonden op index {i}")
            return i
        cap.release()
    print("Geen werkende camera gevonden!")
    return None

def detect_with_yolo_realtime(model_path="yolov8n.pt", source=0):
    model = YOLO(model_path)
    
    try:
        source = int(source)
    except ValueError:
        pass 

    print(f"[DEBUG] Probeer camera te openen via: {source}")
    cap = cv2.VideoCapture(source)
    
    if not cap.isOpened():
        print("Fout: Kan de camera niet openen!")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Geen frame ontvangen! Controleer je camera.")
            break

        results = model(frame)
        for result in results:
            for box, cls in zip(result.boxes.xyxy, result.boxes.cls):
                x1, y1, x2, y2 = map(int, box)
                label = model.names[int(cls)]
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(frame, label, (x1, y1 - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        cv2.imshow("YOLOv8 Realtime Detectie", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

def detect_with_hailo_realtime(model_path="yolov8n.hef", source=0):
    if not HAILO_AVAILABLE:
        print("Hailo SDK is niet geïnstalleerd! Gebruik de CPU/GPU modus.")
        return

    inferencer = Inferencer(model_path)
    cap = cv2.VideoCapture(source)

    if not cap.isOpened():
        print("Fout bij openen van videostream!")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            print("⚠️ Geen frame ontvangen!")
            break

        results = inferencer.infer(frame)
        for detection in results["detections"]:
            x1, y1, x2, y2 = map(int, detection["bbox"])
            label = detection["label"]
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
            cv2.putText(frame, label, (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

        cv2.imshow("Hailo AI Realtime Detectie", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=str, default=None, help="Videobron (0=webcam, /dev/videoX of IP-camera URL)")
    parser.add_argument("--hailo", action="store_true", help="Gebruik Hailo-versnelling (als beschikbaar)")
    args = parser.parse_args()

    if args.source is None:
        args.source = find_first_working_camera()
        if args.source is None:
            print("Geen beschikbare camera gevonden. Stoppen.")
            exit()

    if args.hailo:
        detect_with_hailo_realtime(source=args.source)
    else:
        detect_with_yolo_realtime(source=args.source)
