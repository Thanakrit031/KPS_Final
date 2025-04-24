from ultralytics import YOLO
from picamera2 import Picamera2, Preview
import cv2

# Initialize the camera
picam2 = Picamera2()
picam2.configure(picam2.create_preview_configuration(main={"size": (2304, 1296), "format": "RGB888"}))
picam2.set_controls({"AfMode": 2, "ExposureValue": 1})
picam2.start()

# Load the trained YOLO model
model = YOLO("/home/kps/Downloads/288*288 crop+brightness/best.pt")

class_names = ["Class_A", "Class_B", "Class_C"]

try:
    while True:
        # Capture and preprocess frame
        frame = picam2.capture_array()

        # Run prediction
        results = model.predict(frame, imgsz=288)
        # results = model.predict(frame, imgsz=288)

        # Process results
        for result in results:
            if result.boxes is not None:
                for box in result.boxes:
                    x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
                    class_id = int(box.cls.cpu().numpy()[0])
                    conf = float(box.conf.cpu().numpy()[0])
                    # Get the class name from class_id
                    class_name = class_names[class_id]  # Use class_names list to map ID to name
                    print(f"Detected: {class_name}, Confidence: {conf:.2f}")

                    # Optionally, draw the bounding box and class name
                    x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cv2.putText(frame, f"{class_name} {conf:.2f}", (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        
        # Show output
        # output_frame = cv2.resize(frame ,(640, 640))
        cv2.imshow("YOLO Detection", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

except Exception as e:
    print(f"Error occurred: {e}")

finally:
    picam2.stop()
    cv2.destroyAllWindows()
