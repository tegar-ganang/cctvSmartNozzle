from flask import Flask, render_template, Response,request
from flask_sse import sse
import time
from src.main_runtime import *
from src.camera_runtime import *
import webbrowser


app = Flask(__name__)
app.config["REDIS_URL"] = "redis://localhost"
app.register_blueprint(sse, url_prefix="/stream")
camera =CameraOBJ()

def get_ai_data():
    while True:
        data = f"{camera.license_plate};{camera.status_subsidi}" 
        yield f"data: {data}\n\n"
        time.sleep(1)




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

@app.route('/')
def index():
    return render_template('main.html')





if __name__ == '__main__':
    app.run(debug=True)