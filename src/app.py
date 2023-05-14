import cv2
import base64
from flask import Flask, render_template, request, jsonify
from ultralytics import YOLO
import numpy as np
# import request

app = Flask(__name__, static_url_path='/static')

# Load the YOLOv8 model
from roboflow import Roboflow
rf = Roboflow(api_key="XxSTtrAZ8RK9T04qvhJb")
project = rf.workspace().project("bowdetector")
model = project.version(1).model




midpoints = []

@app.route('/')
def index():
    return render_template('index.html')

ROBOFLOW_API_KEY = "XxSTtrAZ8RK9T04qvhJb"
ROBOFLOW_MODEL = model
ROBOFLOW_SIZE = 416

upload_url = "".join([
    "https://detect.roboflow.com/",
    ROBOFLOW_MODEL,
    "?access_token=XxSTtrAZ8RK9T04qvhJb",
    ROBOFLOW_API_KEY,
    "&format=image",
    "&stroke=5"
])

video = cv2.VideoCapture(0)

@app.route('/infer', methods=['POST', 'OPTIONS'])
# Infer via the Roboflow Infer API and return the result
def infer():
    # Get the current image from the webcam
    ret, img = video.read()

    # Resize (while maintaining the aspect ratio) to improve speed and save bandwidth
    height, width, channels = img.shape
    scale = ROBOFLOW_SIZE / max(height, width)
    img = cv2.resize(img, (round(scale * width), round(scale * height)))

    # Encode image to base64 string
    retval, buffer = cv2.imencode('.jpg', img)
    img_str = base64.b64encode(buffer)

    # Get prediction from Roboflow Infer API
    resp = requests.post(upload_url, data=img_str, headers={
        "Content-Type": "application/x-www-form-urlencoded"
    }, stream=True).raw

    # Parse result image
    image = np.asarray(bytearray(resp.read()), dtype="uint8")
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)

    return image




# detection_count = 0  # Initialize a counter variable outside the function

# @app.route('/detect', methods=['POST', 'OPTIONS'])
# def detect():

#     global detection_count  # Declare the counter variable as global to modify it

#     # Get the base64-encoded frame from the request
#     frame_data = request.form['frame']
#     frame_encoded = frame_data.split(',')[1]
#     frame_bytes = base64.b64decode(frame_encoded)

#     # Decode the frame into a NumPy array and convert the color format
#     frame = cv2.imdecode(np.frombuffer(frame_bytes, dtype=np.uint8), -1)
#     frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

#     # Run YOLOv8 inference on the frame
#     results = model(frame)

#     # Visualize the results on the frame
#     annotated_frame = results[0].plot()

#     boxes = results[0].boxes
#     labels = results[0].names

#     for box in boxes:
#         # Get the XYXY values
#         top, left, bottom, right = [_.item() for _ in box.xyxy[0]]

#         label = labels[box.cls.item()]
#         conf = box.conf.item()

#         if label == 'bow':
#             bow_midpoint = (int((top + bottom) // 2), int((left + right) // 2))
#             midpoints.append(bow_midpoint)
#             # Draw a circle at the calculated midpoint
#             cv2.circle(annotated_frame, bow_midpoint, radius=5, color=(0, 0, 255), thickness=-1)


#         elif label == 'bridge':
#             bridge_midpoint = ((left + right) // 2, (top + bottom) // 2)

#     if len(midpoints) > 1:
#         # Draw a line connecting all the midpoints
#         midpoints_array = np.array(midpoints, dtype=np.int32)
#         cv2.polylines(annotated_frame, [midpoints_array], False, (0, 255, 0), thickness=2)

#     # Increment the detection counter
#     detection_count += 1

#     # If the detection counter reaches 60, clear the midpoints list and reset the counter
#     if detection_count >= 23:
#         midpoints.clear()
#         detection_count = 0

#     # Convert the color format back to BGR
#     annotated_frame = cv2.cvtColor(annotated_frame, cv2.COLOR_RGB2BGR)

#     # Encode the annotated frame as a JPEG image
#     _, buffer = cv2.imencode('.jpg', annotated_frame)
#     annotated_frame_bytes = buffer.tobytes()

#     # Encode the annotated frame as a base64 string
#     annotated_frame_data = base64.b64encode(annotated_frame_bytes).decode('utf-8')

#     # Return the annotated frame to the client
#     return jsonify({'frame': 'data:image/jpeg;base64,' + annotated_frame_data})

# if __name__ == '__main__':
#     app.run(debug=True)







