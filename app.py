from flask import Flask, Response , render_template
import cv2 as cv
from ultralytics import YOLO
from datetime import datetime
import math,time,os,threading


app = Flask(__name__)

# SETTING

ALERT_FOLDER = "static/alerts"
THRESHOLD_DISTANCE = 150
ALERT_COOLDOWN = 20
os.makedirs(ALERT_FOLDER , exist_ok=True)


capture = None
model1 = None
model2 = None

def initialize():
    global capture, model1, model2

    print("Opening camera...")
    capture = cv.VideoCapture(0)

    print("Loading model1...")
    model1 = YOLO("models/yolov8n.pt")

    print("Loading model2...")
    model2 = YOLO("models/best.pt")

    print("Initialization complete")



def current_time():
    return datetime.now().strftime("%d-%m-%Y_%H-%M-%S")

def file_time():
    return datetime.now().strftime("%d-%m-%Y_%H-%M-%S")


# Distance calculation function

def distance(box1, box2):
    x1, y1, x2, y2 = box1
    a1, b1, a2, b2 = box2

    cx1 = (x1 + x2) // 2
    cy1 = (y1 + y2) // 2

    cx2 = (a1 + a2) // 2
    cy2 = (b1 + b2) // 2

    return math.sqrt((cx2 - cx1) ** 2 + (cy2 - cy1) ** 2)


def generate_frames():
    print("GENERATE FRAMES CALLED")

    # initial confirm count is 0

    confirm_count = 0
    last_alert_time = 0

    if not capture.isOpened():
        print("Camera not opened")
        exit()


    # MAIN LOOP

    while True:
        try:
            ret, frame = capture.read()
            if not ret:
                break
            frame = cv.flip(frame, 1)
            frame = cv.resize(frame , (800,600))

            person_boxes = []
            weapon_boxes = []

            threat_detected = False

            # PERSON DETECTION

            result1 = model1(frame)

            for r in result1:
                boxes = r.boxes
                for box in boxes:
                    cls_id = int(box.cls.item())
                    conf = float(box.conf.item())
                    if cls_id == 0 and conf > 0.5:
                        x1, y1, x2, y2 = map(int, box.xyxy[0])
                        person_boxes.append((x1, y1, x2, y2))
                        cv.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                        cv.putText(frame, "Person", (x1, y1 - 10), cv.FONT_HERSHEY_COMPLEX, 2, (0, 0, 255), 2)


            # WEAPON DETECTION

            result2 = model2(frame)

            for r in result2:
                boxes = r.boxes
                for box in boxes:
                    cls_id = int(box.cls.item())
                    conf = float(box.conf.item())
                    if cls_id in [0, 1] and conf > 0.4:
                        x1, y1, x2, y2 = map(int, box.xyxy[0])
                        weapon_boxes.append((x1, y1, x2, y2))
                        cv.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)
                        cv.putText(frame, f"{model2.names[cls_id]}", (x1, y1 - 10), cv.FONT_HERSHEY_COMPLEX, 2, (0, 0, 139), 2)



            # DISTANCE CHECK

            for p in person_boxes:
                for w in weapon_boxes:
                    dist = distance(p, w)
                    if dist < THRESHOLD_DISTANCE:
                        threat_detected = True





            # 3 FRAME CONFIRMATION

            if threat_detected:
                confirm_count += 1
            else:
                confirm_count = 0

            # ALERT

            if confirm_count >= 3:
                cv.putText(frame, "ALERT! WEAPON NEAR PERSON", (30, 50), cv.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 3)

            # SAVE ONLY ONCE
            now = time.time()

            if confirm_count == 3 and (now - last_alert_time) > ALERT_COOLDOWN:
                last_alert_time = now

                filename = f"{ALERT_FOLDER}/alert_{file_time()}.jpg"
                cv.imwrite(filename, frame)
                from utils.alerts import send_whatsapp, send_email, send_alarm
                # run in threads
                threading.Thread(target=send_alarm).start()
                threading.Thread(target=send_email).start()
                threading.Thread(target=send_whatsapp).start()


            # TIME ON SCREEN

            cv.putText(frame , current_time() , (20,580) , cv.FONT_HERSHEY_COMPLEX , 0.6 , (255,255,255) , 2)

            # ENCODE FRAME
            ret,buffer = cv.imencode('.jpg' , frame)
            frame = buffer.tobytes()

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        except Exception as e:
            print("ERROR: " , e)
            continue

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video')
def video():
    return Response(generate_frames() , mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":

    if os.environ.get("WERKZEUG_RUN_MAIN") == "true":
        initialize()
    app.run(debug=True)
