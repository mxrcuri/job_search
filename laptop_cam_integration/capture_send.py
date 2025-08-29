import cv2
import requests
import time

url = "https://bright-hounds-cheat.loca.lt/upload_frame"

cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Failed to open camera.")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        continue

    _, buf = cv2.imencode('.jpg', frame)
    
    try:
        headers = {"User-Agent": "PawOS-Camera-Client/1.0"}
        response = requests.post(url, files={'frame': buf.tobytes()}, headers=headers)
        print("Server response:", response.json())
    except Exception as e:
        print("Error sending frame:", e)

    time.sleep(1)
