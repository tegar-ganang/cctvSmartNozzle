import webbrowser
import cv2
import time
from flask import Flask, render_template, Response,request
from flask_sse import sse
from src.main_runtime import *
from src.camera_runtime import *

from transformers import VisionEncoderDecoderModel
object_detection_model = VisionEncoderDecoderModel.from_pretrained("C:\\Users\\OSVALDO KURNIAWAN\\Downloads\\model_base_modify_augmented4k-20230905T100732Z-001\\model_base_modify_augmented4k")

# from detectron2.utils.visualizer import Visualizer, ColorMode
# from detectron2.config import get_cfg
# from detectron2.data import MetadataCatalog
# from detectron2.engine import DefaultPredictor
# cfg = get_cfg()
# cfg.merge_from_file("/path/to/config.yaml")  # Replace with the path to your model's config file
# cfg.MODEL.WEIGHTS = "/path/to/model.pth"  # Replace with the path to your model's weights
# cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.5  # Set a threshold for detection scores
# predictor = DefaultPredictor(cfg)
# object_detection_model = ObjectDetectionModel()
# object_detection_model.load_weights('"C:\Users\OSVALDO KURNIAWAN\Downloads\modelv1.pt"')

app = Flask(__name__)
app.config["REDIS_URL"] = "redis://localhost"
app.register_blueprint(sse, url_prefix="/stream")
camera =CameraOBJ()

def draw_boxes(frame, detections):
    for detection in detections:
        label = detection['label']
        confidence = detection['confidence']
        bbox = detection['bbox']
        
        # Convert bbox from relative coordinates to absolute pixel values
        height, width, _ = frame.shape
        x1, y1, x2, y2 = int(bbox[0] * width), int(bbox[1] * height), int(bbox[2] * width), int(bbox[3] * height)
        
        # Draw bounding box
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        
        # Display label and confidence
        label_text = f"{label}: {confidence:.2f}"
        cv2.putText(frame, label_text, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    
    return frame

def get_ai_data():
    while True:
        frame = camera.capture_frame()
        detections = object_detection_model.detect_objects(frame)
        processed_frame = draw_boxes(frame, detections)

        ret, jpeg = cv2.imencode('.jpg', processed_frame)
        frame_bytes = jpeg.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

#INI BAGIAN ROUTE UNTUK WEB APABILA INGIN MENAMBAH BOLEHH
@app.route('/video_feed')
def video_feed():
    def generate():
        for frame in camera.capture_runtime():
            detections = object_detection_model.detect_objects(frame)
            processed_frame = draw_boxes(frame, detections)

            ret, jpeg = cv2.imencode('.jpg', processed_frame)
            frame_bytes = jpeg.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

    return Response(generate(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route("/send_detect_information")
def send_detect_information():
    def generate_ai_data():
        while True:
            frame = camera.capture_frame()
            detections = object_detection_model.detect_objects(frame)
            object_info = []

            for detection in detections:
                label = detection['label']
                confidence = detection['confidence']
                bbox = detection['bbox']
                object_info.append(f"{label}: {confidence:.2f}")

            object_data = ', '.join(object_info)
            data = f"Plat Nomor: {camera.license_plate}; Status: {camera.status_subsidi}; Objects Detected: {object_data}"
            
            yield f"data: {data}\n\n"
            time.sleep(1)

    return Response(generate_ai_data(), mimetype="text/event-stream")

@app.route('/dashboard_request', methods=['POST'])
def dashboard_request():
    data_web = request.json['input_string']
    callback(data=data_web)
    return data_web

@app.route('/')
def index():
    return render_template('main.html')

if __name__ == '__main__':
    app.run(debug=True)
