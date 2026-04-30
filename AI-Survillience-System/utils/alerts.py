import smtplib
import time
from email.mime.text import MIMEText
import pywhatkit as kit
import playsound
from datetime import datetime




# Current Time
def current_time():
    return datetime.now().strftime("%d-%m-%Y %H:%M:%S")


EMAIL_USER = "yourgmail@gmail.com"
APP_PASSWORD = "your-app-password"
EMAIL_TO = "receivergmail@gmail.com"


# Sending Email
def send_email():
    try:
        msg = MIMEText(f"Weapon Detected Near Person!\nTime:{current_time()}")
        msg["Subject"] = "ALERT"
        msg["From"] = EMAIL_USER
        msg["To"] = EMAIL_TO

        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(EMAIL_USER, APP_PASSWORD)
        server.sendmail(EMAIL_USER, EMAIL_TO, msg.as_string())
        server.quit()
        print("EMAIL SENT")

    except Exception as e:
        print("Email Error:", e)


WHATSAPP_NO = "+923XXXXXXXXX"


# Send Whatsapp
def send_whatsapp():
    try:
        kit.sendwhatmsg_instantly(WHATSAPP_NO, f"Weapon Detected Near Person!\nTime:{current_time()}")
        print("WHATSAPP SENT")
    except Exception as e:
        print("Whatsapp Error:", e)


AUDIO = "audio/faah.mp3"


# send alarm
def send_alarm():
    try:
        for _ in range(3):
            playsound.playsound(AUDIO)
            time.sleep(1)
    except Exception as e:
        print("Sound Error:", e)
