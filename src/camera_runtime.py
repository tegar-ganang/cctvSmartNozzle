import cv2
import numpy as np
import requests
from roboflow import Roboflow
import time
from transformers import VisionEncoderDecoderModel
from PIL import Image
import torch
from torchvision import transforms

model = VisionEncoderDecoderModel.from_pretrained("C:\\Users\\OSVALDO KURNIAWAN\\Documents\\PKMSmartNozzle\\SmartNozzle\\CCTV-integrated model 1\\src\\model_base_modify_augmented4k", local_files_only=True)

class CameraOBJ:
    def __init__(self):
        # self.machine_capture = cv2.VideoCapture('rtsp://admin:HIEEJC@169.254.94.233:554')
        self.machine_capture = cv2.VideoCapture(0)
        self.detect_status  = 0
        self.original_image = np.zeros((1080, 1920, 3), dtype=np.uint8)
        self.output_frame = np.zeros((480, 270, 3), dtype=np.uint8)
        self.status_subsidi = 0
        self.jenis_mobil = f"Predict ..."
        self.license_plate = f"K {np.random.randint(1000, 5555)} ASF"
        self.detect_toggle_timer = time.time()
        self.detect_toggle_interval = 10  # interval
        self.rf = Roboflow(api_key="0luIXfVr4TvXOnHEZrhm")
        self.project = self.rf.workspace().project("car_detect-ao4mr")
        self.model = self.project.version(1).model

    def switch_detect_status(self):
        self.detect_status = not self.detect_status

    def send_frame_to_roboflow(self, frame):
        # Perform object detection on the frame and return the JSON response
        response = self.model.predict(frame, confidence=60, overlap=40).json()

        if "predictions" in response and len(response["predictions"]) > 0:
            class_value = response["predictions"][0]["class"]
            self.jenis_mobil = f"{class_value}"  # Assuming you want to format it as 'K {class_value} ASF'
            if self.jenis_mobil == "Honda Brio" or self.jenis_mobil == "Honda Jazz" or self.jenis_mobil == "Toyota Avanza":
                self.status_subsidi = 1
            else :
                self.status_subsidi = 0
        print(response, self.status_subsidi)

        return response
    
    def capture_runtime(self):
        while True:
            # Check if it's time to toggle detect status
            if time.time() - self.detect_toggle_timer >= self.detect_toggle_interval:
                self.switch_detect_status()
                self.detect_toggle_timer = time.time()

            success, frame = self.machine_capture.read()
            if not success:
                break
            else:
                if self.detect_status == 0:
                    self.output_frame = cv2.resize(frame, (480, 270))
                else:
                    # Send the frame to Roboflow for object detection
                    self.status_subsidi = 0
                    self.jenis_mobil = f"Predict ..."
                    detection_result = self.send_frame_to_roboflow(frame)
                    self.detect_car_license(frame)

                    # Update the output frame with the processed frame
                    self.output_frame = cv2.resize(frame, (480, 270))
                    self.switch_detect_status()

                ret, buffer = cv2.imencode('.jpg', self.output_frame)
                frame = buffer.tobytes()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    def detect_car_license(self, frame):
        # Convert the frame to a PIL Image
        image_pil = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

        # Define a transformation to preprocess the image
        preprocess = transforms.Compose([
            transforms.Resize((384, 384)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ])

        # Preprocess the image and convert it to a tensor
        input_image = preprocess(image_pil).unsqueeze(0)  # Add a batch dimension

        # Process the image using the model to generate a caption
        generated_ids = model.generate(input_image)
        generated_text = model.processor.batch_decode(generated_ids, skip_special_tokens=True)[0]

        container_detect_car_license = np.zeros((1080, 1920, 3), dtype=np.uint8)
        
        # Update the class attributes
        self.license_plate = generated_text
        self.output_frame = cv2.resize(container_detect_car_license, (480, 270))