import sys
#Change the following line
sys.path.append('C:\Python310\Lib\site-packages\cv2')

import numpy as np
import cv2

import mediapipe as mp

import time



#import socket

#

#HOST = "127.0.0.1"  # The server's hostname or IP address

#PORT = 8052  # The port used by the server

#

#with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:

#    s.connect((HOST, PORT))

#    s.sendall(b"Hello, world")

#    data = s.recv(1024)

#

#print(f"Received {data!r}")





mpPose = mp.solutions.pose
pose = mpPose.Pose()
mpDraw = mp.solutions.drawing_utils



cap = cv2.VideoCapture(1)
# cap = cv2.VideoCapture('a.mp4')

pTime = 0



while True:
    success, img = cap.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = pose.process(imgRGB)
    print(results.pose_landmarks)
    if results.pose_landmarks:
        mpDraw.draw_landmarks(img, results.pose_landmarks, mpPose.POSE_CONNECTIONS)
        for id, lm in enumerate(results.pose_landmarks.landmark):
            h, w, c = img.shape
            print(id, results.pose_landmarks.landmark[0].x)
            cx, cy = int(lm.x*w), int(lm.y*h)
            cv2.circle(img, (cx, cy), 5, (255,0,0), cv2.FILLED)

    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime

    cv2.putText(img, str(int(fps)), (50,50), cv2.FONT_HERSHEY_SIMPLEX,1,(255,0,0), 3)
    cv2.imshow("Image", img)
    cv2.waitKey(1)

