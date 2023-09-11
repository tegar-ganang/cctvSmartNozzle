# !pip install roboflow
import os
import json
from roboflow import Roboflow
rf = Roboflow(api_key="0luIXfVr4TvXOnHEZrhm")
project = rf.workspace().project("car_detect-ao4mr")
model = project.version(1).model
path = "C:\\Users\\OSVALDO KURNIAWAN\\Documents\\PKMSmartNozzle\\SmartNozzle\\CCTV\\src"
target_path = "C:\\Users\\OSVALDO KURNIAWAN\\Documents\\PKMSmartNozzle\\SmartNozzle\\CCTV\\src\\res.json"

# infer on a local image
pred = model.predict("scene01461.png", confidence=70, overlap=30).json()

def safe_create_path_parent(path: str) -> None:
    path_parent = os.path.dirname(path)
    os.makedirs(path_parent, exist_ok=True)

def dump_to_json(target_path: str, content: dict) -> None:
    safe_create_path_parent(target_path)
    with open(target_path, 'w') as outfile:
        json.dump(content, outfile, indent=4)

dump_to_json(target_path, pred)

# visualize your prediction

# model.predict("your_image.jpg", confidence=40, overlap=30).save("prediction.jpg")

# infer on an image hosted elsewhere
# print(model.predict("C:\Users\OSVALDO KURNIAWAN\Documents\PKM - Smart Nozzle\Smart Nozzle\CCTV\img", hosted=True, confidence=40, overlap=30).json())