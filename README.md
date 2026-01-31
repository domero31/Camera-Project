# 📷 AI Security Camera System

A real-time security monitoring application built with Python. This system uses computer vision (YOLOv8) to detect intruders and instantly sends photo alerts to a Telegram mobile app.

## 🚀 Features
* **Real-time Detection:** Uses the YOLOv8 AI model to detect humans with high accuracy.
* **Instant Alerts:** Sends a photo notification to your phone via Telegram bot within seconds of detection.
* **Smart Cooldown:** Includes logic to prevent spamming notifications (defaults to one alert every 15 seconds).
* **Privacy Secure:** API keys and sensitive credentials are managed via environment variables (.env).

## 🛠️ Tech Stack
* **Language:** Python 3.12
* **Computer Vision:** OpenCV (`cv2`)
* **AI Model:** Ultralytics YOLOv8 (Nano)
* **Notifications:** Telegram Bot API
* **Dependency Management:** uv

## 💻 How It Works
1.  The script captures video frames from the primary webcam.
2.  Each frame is processed by the YOLOv8 neural network to identify objects.
3.  If a person (Class 0) is detected with >50% confidence:
    * The system checks the last alert timestamp.
    * If the cooldown period has passed, it captures the frame.
    * The frame is uploaded to the Telegram API and delivered to the user.

## 🔐 Setup
*(Note: You need a `.env` file to run this locally)*
```bash
TELEGRAM_TOKEN=your_token_here
TELEGRAM_CHAT_ID=your_chat_id_here
