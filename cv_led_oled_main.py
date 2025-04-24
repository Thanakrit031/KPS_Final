from ultralytics import YOLO
from picamera2 import Picamera2
import cv2
import gpiod
import time
import board
import busio
import adafruit_ssd1306
from PIL import Image, ImageDraw, ImageFont

# ---------- Setup OLED ----------
i2c = busio.I2C(board.SCL, board.SDA)
oled = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c)

# Clear screen and prepare drawing surface
oled.fill(0)
oled.show()
image = Image.new("1", (128, 32))
draw = ImageDraw.Draw(image)

# Load font
try:
    font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 31)
except IOError:
    font = ImageFont.load_default()

# ---------- Setup GPIO LEDs ----------
LED_PINS = {"Class_A": 17, "Class_B": 27, "Class_C": 22}
chip = gpiod.Chip('gpiochip4')
led_lines = {cls: chip.get_line(pin) for cls, pin in LED_PINS.items()}

for line in led_lines.values():
    line.request(consumer="LED", type=gpiod.LINE_REQ_DIR_OUT)

# ---------- Setup Camera ----------
picam2 = Picamera2()
picam2.configure(picam2.create_preview_configuration(main={"size": (2304, 1296), "format": "RGB888"}))
picam2.set_controls({"AfMode": 2, "ExposureValue": 1})
picam2.start()

# ---------- Load YOLO Model ----------
model = YOLO("best.pt")
class_names = ["Class_A", "Class_B", "Class_C"]
prev_class = None

# ---------- Detection Function ----------
def detect_objects(frame):
    results = model.predict(frame, max_det=1, imgsz=288)
    for result in results:
        if result.boxes and len(result.boxes) > 0:
            box = result.boxes[0]
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            class_id = int(box.cls[0])
            conf = float(box.conf[0])
            class_name = class_names[class_id]

            # Draw box and label
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, f"{class_name} {conf:.2f}", (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 2.5, (0, 255, 0), 3)

            print(f"Detected: {class_name}, Confidence: {conf:.2f}")
            return class_name
    return None

# ---------- Main Loop ----------
try:
    while True:
        frame = picam2.capture_array()
        detected = detect_objects(frame)

        # Control LEDs
        for cls, line in led_lines.items():
            line.set_value(1 if detected == cls else 0)

        # OLED Display
        if detected != prev_class:
            oled.fill(0)
            draw.rectangle((0, 0, 128, 32), fill=0)
            if detected:
                draw.text((55, 0), detected[-1], font=font, fill=255)
            oled.image(image)
            oled.show()
            prev_class = detected

        # Show camera frame
        cv2.imshow("YOLO Detection", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

# ---------- Error Handling ----------
except Exception as e:
    print(f"Error: {e}")

# ---------- Cleanup ----------
finally:
    picam2.stop()
    cv2.destroyAllWindows()
    for line in led_lines.values():
        line.set_value(0)
        line.release()
    chip.close()
    oled.fill(0)
    oled.show()
