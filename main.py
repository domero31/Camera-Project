import cv2
import time
import requests
from ultralytics import YOLO

# --- 🔐 YOUR TELEGRAM KEYS ---
# I pasted your new token below:
BOT_TOKEN = "8565697502:AAF3N9eBcEbcous8_YpYGk4pXI8QFy6lKiU"
CHAT_ID = "6698024037"

def send_telegram_alert(frame):
    """Sends the photo to your phone"""
    msg = "🚨 Intruder Detected!"
    
    # Save & Send
    cv2.imwrite("alert.jpg", frame)
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"
    with open("alert.jpg", "rb") as photo:
        print("Attempting to send to Telegram...")
        response = requests.post(url, data={"chat_id": CHAT_ID, "caption": msg}, files={"photo": photo})
        
        if response.status_code == 200:
            print("✅ SUCCESS: Photo sent to your phone!")
        else:
            print(f"❌ ERROR: {response.text}")

# Load model
model = YOLO("yolov8n.pt")
cap = cv2.VideoCapture(0)

print("✅ Security Camera Active. Press Q to quit.")
last_alert_time = 0
alert_cooldown = 15

while True:
    ret, frame = cap.read()
    if not ret: break

    results = model(frame, verbose=False)[0]
    person_detected = False

    if results.boxes is not None:
        for box in results.boxes:
            if int(box.cls[0].item()) == 0 and float(box.conf[0].item()) >= 0.5:
                person_detected = True
                x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(frame, "Person", (x1, y1 - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

    if person_detected:
        if time.time() - last_alert_time > alert_cooldown:
            print("🚨 ALERT: Detecting person...")
            try:
                send_telegram_alert(frame)
            except Exception as e:
                print(f"❌ System Error: {e}")
            last_alert_time = time.time()

    cv2.imshow("Security Camera", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
