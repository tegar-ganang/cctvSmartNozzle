import cv2
import numpy as np


class CameraOBJ:
    def __init__(self):
        self.machine_capture = cv2.VideoCapture('rtsp://admin:HIEEJC@169.254.94.233:554')
        self.detect_status  = 0
        self.original_image = np.zeros((1080, 1920,3), dtype=np.uint8)
        self.output_frame = np.zeros((480, 270,3), dtype=np.uint8)
        self.status_subsidi = 1
        self.license_plate = f"K {np.random.randint(1000, 5555)} ASF"

    
    def switch_detect_status(self):
        self.detect_status = not self.detect_status

    def capture_runtime(self):
        while True:
            success, frame = self.machine_capture.read()
            if not success:
                break
            else:
                if self.detect_status == 0 :
                    self.output_frame = cv2.resize(frame, (480, 270))
                else:
                    self.detect_car_license()

                ret, buffer = cv2.imencode('.jpg', self.output_frame)
                frame = buffer.tobytes()
                yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n') 


    def detect_car_license(self):
        #DISINI ALGORITMA UNTUK MENDETEKSI PLAT NOMOR, JENIS KENDARAAN
        container_detect_car_license = np.zeros((1080, 1920,3), dtype=np.uint8)
        
        #disini untuk return ke attribute class
        self.status_subsidi = 1
        self.license_plate = f"K {np.random.randint(1000, 5555)} ASF"
        self.output_frame = cv2.resize(container_detect_car_license, (480, 270))