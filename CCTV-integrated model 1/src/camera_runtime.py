import cv2
import numpy as np
import requests
from roboflow import Roboflow

class CameraOBJ:
    def __init__(self):
        self.machine_capture = cv2.VideoCapture('rtsp://admin:HIEEJC@169.254.94.233:554')
        # self.machine_capture = cv2.VideoCapture(0)
        self.detect_status  = 0
        self.original_image = np.zeros((1080, 1920, 3), dtype=np.uint8)
        self.output_frame = np.zeros((480, 270, 3), dtype=np.uint8)
        self.status_subsidi = 1
        self.license_plate = f"K {np.random.randint(1000, 5555)} ASF"

    def switch_detect_status(self):
        self.detect_status = not self.detect_status

    def send_frame_to_roboflow(self, frame):
        rf = Roboflow(api_key="0luIXfVr4TvXOnHEZrhm")
        project = rf.workspace().project("car_detect-ao4mr")
        model = project.version(1).model

        # Perform object detection on the frame and return the JSON response
        response = model.predict(frame, confidence=40, overlap=30).json()

        print(response)

        return response
    
    def capture_runtime(self):
        while True:
            success, frame = self.machine_capture.read()
            if not success:
                break
            else:
                if self.detect_status == 0:
                    self.output_frame = cv2.resize(frame, (480, 270))
                else:
                    # Send the frame to Roboflow for object detection
                    detection_result = self.send_frame_to_roboflow(frame)

                    # Process the detection results (e.g., draw bounding boxes)
                    # self.process_detection_results(frame, detection_result)

                    # Update the output frame with the processed frame
                    self.output_frame = cv2.resize(frame, (480, 270))

                ret, buffer = cv2.imencode('.jpg', self.output_frame)
                frame = buffer.tobytes()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    def process_detection_results(self, frame, detection_result):
        # Implement logic to process the detection results (e.g., draw bounding boxes)
        # You need to parse the 'detection_result' JSON and draw bounding boxes on 'frame'
        # Example:
        for detection in detection_result["predictions"]:
            x1, y1, x2, y2 = detection_result["xmin"], detection_result["ymin"], detection_result["xmax"], detection_result["ymax"]
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)  # Draw a green rectangle

    def detect_car_license(self):
        # DISINI ALGORITMA UNTUK MENDETEKSI PLAT NOMOR, JENIS KENDARAAN
        container_detect_car_license = np.zeros((1080, 1920, 3), dtype=np.uint8)
        
        # disini untuk return ke attribute class
        self.status_subsidi = 1
        self.license_plate = f"K {np.random.randint(1000, 5555)} ASF"
        self.output_frame = cv2.resize(container_detect_car_license, (480, 270))
