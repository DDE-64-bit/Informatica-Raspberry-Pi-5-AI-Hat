import cv2
from ultralytics import YOLO
import argparse

# Probeer Hailo SDK te importeren
try:
    from hailo_sdk_client import Inferencer
    HAILO_AVAILABLE = True
except ImportError:
    HAILO_AVAILABLE = False
    print("Hailo SDK niet gevonden, alleen CPU/GPU modus beschikbaar!")

# Functie om YOLOv8 te gebruiken zonder Hailo (standaard CPU/GPU)
def detect_with_yolo(image_path, model_path="yolov8x.pt"):
    model = YOLO(model_path)  # YOLOv8 nano model (downloadt automatisch)
    image = cv2.imread(image_path)  # Laad de afbeelding
    results = model(image)  # Voer objectdetectie uit

    # Teken de detecties op de afbeelding
    for result in results:
        for box, cls in zip(result.boxes.xyxy, result.boxes.cls):
            x1, y1, x2, y2 = map(int, box)
            label = model.names[int(cls)]  # Objectnaam
            cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(image, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    cv2.imshow("YOLOv8 Detectie (CPU/GPU)", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


# Functie om YOLOv8 met Hailo versnelling te gebruiken
def detect_with_hailo(image_path, model_path="yolov8n.hef"):
    if not HAILO_AVAILABLE:
        print("Hailo SDK is niet geïnstalleerd! Gebruik de CPU/GPU modus.")
        return

    inferencer = Inferencer(model_path)  # Laad het Hailo-geoptimaliseerde model
    image = cv2.imread(image_path)  # Laad de afbeelding

    # Voer inferentie uit
    results = inferencer.infer(image)

    # Teken de detecties op de afbeelding
    for detection in results["detections"]:
        x1, y1, x2, y2 = map(int, detection["bbox"])
        label = detection["label"]
        cv2.rectangle(image, (x1, y1), (x2, y2), (0, 0, 255), 2)
        cv2.putText(image, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

    cv2.imshow("Hailo AI Detectie", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


# Hoofdprogramma om te kiezen tussen CPU/GPU en Hailo
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("image", help="Pad naar de afbeelding die geanalyseerd moet worden")
    parser.add_argument("--hailo", action="store_true", help="Gebruik Hailo-versnelling (als beschikbaar)")
    args = parser.parse_args()

    if args.hailo:
        detect_with_hailo(args.image)
    else:
        detect_with_yolo(args.image)
