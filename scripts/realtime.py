import cv2
import torch
from ultralytics import YOLO
import argparse

# Probeer Hailo SDK te importeren
try:
    from hailo_sdk_client import Inferencer
    HAILO_AVAILABLE = True
except ImportError:
    HAILO_AVAILABLE = False
    print("⚠️ Hailo SDK niet gevonden, alleen CPU/GPU modus beschikbaar!")

# Functie om YOLOv8 realtime (CPU/GPU) te gebruiken
def detect_with_yolo_realtime(model_path="yolov8n.pt", source=0):
    model = YOLO(model_path)  # Laad YOLOv8 model
    
    cap = cv2.VideoCapture(source, cv2.CAP_DSHOW)  # Open de camera met DirectShow backend (Windows)
    
    if not cap.isOpened():
        print("Fout: Kan de camera niet openen!")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Waarschuwing: Geen frame ontvangen! Controleer of de camera goed werkt.")
            break

        results = model(frame)  # Voer objectdetectie uit

        # Teken de detecties op het frame
        for result in results:
            for box, cls in zip(result.boxes.xyxy, result.boxes.cls):
                x1, y1, x2, y2 = map(int, box)
                label = model.names[int(cls)]  # Objectnaam
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        cv2.imshow("YOLOv8 Realtime Detectie", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):  # Stoppen met 'q'
            break

    cap.release()
    cv2.destroyAllWindows()


# Functie om YOLOv8 met Hailo versnelling in realtime te gebruiken
def detect_with_hailo_realtime(model_path="yolov8n.hef", source=0):
    if not HAILO_AVAILABLE:
        print("Hailo SDK is niet geïnstalleerd! Gebruik de CPU/GPU modus.")
        return

    inferencer = Inferencer(model_path)  # Laad het Hailo-geoptimaliseerde model
    cap = cv2.VideoCapture(source, cv2.CAP_DSHOW)  # Open de camera met DirectShow backend (Windows)
    
    if not cap.isOpened():
        print("Fout bij openen van videostream!")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            print("⚠️ Geen frame ontvangen!")
            break

        results = inferencer.infer(frame)  # Voer inferentie uit

        # Teken de detecties op het frame
        for detection in results["detections"]:
            x1, y1, x2, y2 = map(int, detection["bbox"])
            label = detection["label"]
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
            cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

        cv2.imshow("Hailo AI Realtime Detectie", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):  # Stoppen met 'q'
            break

    cap.release()
    cv2.destroyAllWindows()


# Hoofdprogramma om te kiezen tussen CPU/GPU en Hailo in realtime
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=str, default="0", help="Videobron (0=webcam, of IP-camera URL)")
    parser.add_argument("--hailo", action="store_true", help="Gebruik Hailo-versnelling (als beschikbaar)")
    args = parser.parse_args()

    video_source = int(args.source) if args.source.isdigit() else args.source  # Webcam (0,1..) of IP-camera URL

    if args.hailo:
        detect_with_hailo_realtime(source=video_source)
    else:
        detect_with_yolo_realtime(source=video_source)
