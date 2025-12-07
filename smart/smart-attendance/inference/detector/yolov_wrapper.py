from ultralytics import YOLO


class YOLOv8Wrapper:
    def __init__(self, model_path='yolov8n.pt'):  # use small model for demo
        self.model = YOLO(model_path)

    def detect(self, frame):
        # returns list of dicts: {bbox:[x1,y1,x2,y2], conf, cls}
        results = self.model(frame, imgsz=640, conf=0.4)[0]
        out = []

        for r in results.boxes:
            bbox = r.xyxy[0].cpu().numpy().tolist()  # convert tensor → python list
            conf = float(r.conf[0])                  # detection confidence
            out.append({'bbox': bbox, 'conf': conf})

        return out
