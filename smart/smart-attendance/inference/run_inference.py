import cv2
import requests
import time
import numpy as np

from detector.yolov_wrapper import YOLOv8Wrapper
from recognition.face_encoder import FaceEncoder
from liveness.liveness_model import LivenessModel
from behavior.behavior_model import BehaviorModel


BACKEND_URL = "http://localhost:8000"


def crop_from_bbox(frame, bbox):
    """Crop face region from frame using [x1, y1, x2, y2] bbox."""
    x1, y1, x2, y2 = [int(v) for v in bbox]

    h, w = frame.shape[:2]

    # clamp to frame size (avoid index error)
    x1, x2 = max(0, x1), min(w - 1, x2)
    y1, y2 = max(0, y1), min(h - 1, y2)

    return frame[y1:y2, x1:x2]


def main():
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("❌ Could not open webcam.")
        return

    detector = YOLOv8Wrapper()
    encoder = FaceEncoder()
    liveness = LivenessModel()
    behavior = BehaviorModel()  # currently unused but ready for future

    print("✅ Inference started. Press 'q' to quit.")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("❌ Failed to read frame from webcam.")
            break

        dets = detector.detect(frame)  # YOLO detections
        events = []

        for d in dets:
            face = crop_from_bbox(frame, d["bbox"])

            if face.size == 0:
                continue  # skip invalid crops

            # --- LIVENESS CHECK ---
            live_score = liveness.predict(face)

            event = {
                "bbox": d["bbox"],
                "conf": d["conf"],
                "live_score": live_score,
                "ts": time.time(),  # timestamp
            }

            if live_score > 0.3:
                # Only embed if likely live face
                emb = encoder.embed(face).tolist()
                event["embedding_len"] = len(emb)
                # NOTE: In full system, you'd send the embedding or match it here
            else:
                event["spoof"] = True

            events.append(event)

        # --- SEND EVENTS TO BACKEND ---
        if events:
            for e in events:
                try:
                    requests.post(
                        BACKEND_URL + "/api/events",
                        json=e,
                        timeout=1.0,
                    )
                except Exception as ex:
                    print("Backend post failed:", ex)

        # --- DRAW BBOXES FOR DEBUG ---
        for d in dets:
            x1, y1, x2, y2 = [int(v) for v in d["bbox"]]
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

        cv2.imshow("smart-attendance", frame)

        # Quit on 'q'
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
