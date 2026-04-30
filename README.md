# 🔥 AI Smart Surveillance System (Weapon Detection + Smart Alerts)

## 📌 Overview
This project is a real-time AI-powered surveillance system built using Flask and YOLO-based object detection.  
It monitors live video streams and detects weapons intelligently.

Unlike basic detection systems, this solution reduces false positives by triggering alerts only when a weapon is detected consistently across multiple frames.

---

## 🚀 Features
- 🎯 Real-time weapon detection (YOLO)
- 🧠 Smart alert system (3 consecutive detections logic)
- 📩 Email notifications
- 📲 WhatsApp alerts
- 🔊 Alarm system trigger
- 🌐 Web-based interface (Flask)

---

## 🧰 Tech Stack
- Python  
- Flask  
- OpenCV  
- YOLO (Ultralytics)  

---

## ⚙️ System Workflow
1. Video stream is captured (camera or video input)
2. YOLO model performs object detection on each frame
3. If a weapon is detected in 3 consecutive frames:
   - WhatsApp alert is sent
   - Email notification is triggered
   - Alarm sound is activated
4. If detection is not consistent, alert is ignored (reduces false alarms)

---

## ▶️ Installation

```bash
git clone https://github.com/your-username/AI-Smart-Surveillance-System.git
cd AI-Smart-Surveillance-System
pip install -r requirements.txt
python app.py
