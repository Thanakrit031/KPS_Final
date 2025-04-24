from picamera2 import Picamera2, Preview
import cv2
import os

# Initialize the camera
picam2 = Picamera2()
picam2.configure(picam2.create_preview_configuration(main={"size": (2304, 1296), "format": "RGB888"}))  # For 12MP Camera Module
picam2.set_controls({"AfMode": 2, "ExposureValue": 1})
picam2.start()

# Define the output directory and create it if it does not exist
output_dir = os.path.expanduser('~/project/pictures/New_A')
os.makedirs(output_dir, exist_ok=True)

image_counter = 200  # Counter to keep track of captured images

try:
    while True:
        # Capture a frame from the Raspberry Pi camera
        frame = picam2.capture_array()

        # Display the frame
        cv2.imshow('Camera Feed', frame)

        # Check for user input
        key = cv2.waitKey(1) & 0xFF

        # Capture an image when 'c' is pressed
        if key == ord('c'):
            image_filename = os.path.join(output_dir, f'image_{image_counter:04d}.jpg')
            cv2.imwrite(image_filename, frame)
            print(f"Image captured and saved as {image_filename}")
            image_counter += 1

        # Exit the loop when 'q' is pressed
        if key == ord('q'):
            break
finally:
    # Stop the camera and close OpenCV windows
    picam2.stop()
    cv2.destroyAllWindows() 
