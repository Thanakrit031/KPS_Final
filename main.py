from ultralytics import YOLO
from picamera2 import Picamera2, Preview
import cv2
import time

# Initialize the camera
picam2 = Picamera2()
picam2.configure(picam2.create_preview_configuration(main={"size": (2304, 1296), "format": "RGB888"}))
picam2.set_controls({"AfMode": 2,
   "ExposureValue": 1})
picam2.start()

# Load the trained YOLO model
model = YOLO("/home/kps/Downloads/288*288 crop+brightness/best.pt")

class_names = ["Class_A", "Class_B", "Class_C"]

try:
    while True:
        start_time = time.time()
        # Capture a frame from the Raspberry Pi camera
        frame = picam2.capture_array()
        # Run prediction on the resized frame
        results = model.predict(frame, max_det=1, imgsz=288)
        # Extract and print confidence scores
        for result in results:
            for box in result.boxes:
                class_id = int(box.cls[0])  # Get class ID
                conf = float(box.conf[0])   # Get confidence score
                class_name = class_names[class_id]  # Use class_names list to map ID to name
                print(f"Detected: {class_name}, Confidence: {conf:.2f}")
        end_time = time.time()
        elapsed_time_ms = round((end_time - start_time) * 1000)  # Convert to milliseconds
        print(f"Loop time: {elapsed_time_ms} ms")

except Exception as e:
    print(f"Error occurred: {e}")

finally:
    picam2.stop()
