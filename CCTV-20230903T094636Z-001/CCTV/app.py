from flask import Flask, render_template, Response,request
from flask_sse import sse
import time
from src.main_runtime import *
from src.camera_runtime import *
import webbrowser
import numpy as np
import cv2
import base64
from src.plate_character_detector import PlateCharacterDetector
from src.plate_character_recognizer import PlateCharacterRecognizer
from src.utils import save_plots, create_image_dict


app = Flask(__name__)
app.config["REDIS_URL"] = "redis://localhost"
app.register_blueprint(sse, url_prefix="/stream")
camera =CameraOBJ()

plate_character_detector = PlateCharacterDetector()
plate_character_recognizer = PlateCharacterRecognizer()

def get_ai_data():
    while True:
        data = f"{camera.license_plate};{camera.status_subsidi}" 
        yield f"data: {data}\n\n"
        time.sleep(1)

def process_license_plate(image):
    plate_character_detector.load_image(image=image)
    (character_rois, crop_characters) = plate_character_detector.detect_characters()
    plate_character_recognizer.load_model()
    plate_character_recognizer.load_weights()
    plate_character_recognizer.load_classes_label()

    characters_image = []
    characters = ""

    for character in crop_characters:
        predicted_character, confidence_rate = plate_character_recognizer.predict(
            character)
        characters += predicted_character
        character_label = "{}, {}%".format(
            predicted_character, round(confidence_rate * 100, 2))
        characters_image.append(create_image_dict(
            character, character_label, cmap="gray"))

    crop_characters_plot = save_plots((9, 4), ncols=len(characters_image), nrows=1,
                                      images=characters_image, font_size=9)

    return crop_characters_plot, characters

#INI BAGIAN ROUTE UNTUK WEB APABILA INGIN MENAMBAH BOLEHH
@app.route('/video_feed')
def video_feed():
    return Response(camera.capture_runtime(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route("/send_detect_information")
def send_detect_information():
    return Response(get_ai_data(), mimetype="text/event-stream")

@app.route('/dashboard_request', methods=['POST'])
def dashboard_request():
    data_web = request.json['input_string']
    callback(data=data_web)
    return data_web

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        image_bytes = request.files['license-photo'].read()
        image_array = np.frombuffer(image_bytes, dtype=np.uint8)
        image = cv2.imdecode(image_array, flags=cv2.IMREAD_COLOR)

        crop_characters_plot, characters = process_license_plate(image)

        _, buffer = cv2.imencode('.jpg', img=crop_characters_plot)
        base64_crop_characters_plot = base64.b64encode(buffer).decode("UTF-8")

        _, buffer = cv2.imencode('.jpg', img=image)
        raw_image = base64.b64encode(buffer).decode("UTF-8")

        return render_template('main.html', classified_text=characters)
    
    return render_template('main.html', classified_text=None)





if __name__ == '__main__':
    app.run(debug=True)