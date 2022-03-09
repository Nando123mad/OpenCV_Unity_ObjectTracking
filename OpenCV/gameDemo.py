import sys
#Change the following line
sys.path.append('C:\Python310\Lib\site-packages\cv2')

import numpy as np
import cv2

import mediapipe as mp

import socket
import time


UDP_IP = "127.0.0.1"
UDP_PORT = 5065

print ("UDP target IP:", UDP_IP)
print ("UDP target port:", UDP_PORT)
#print "message:", MESSAGE
#for python 3.7 print("message:",MESSAGE)
sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP

#MediaPipe Pose Data
mpPose = mp.solutions.pose
pose = mpPose.Pose()
mpDraw = mp.solutions.drawing_utils

class App(object):
    def __init__(self, video_src):
        self.cam = cv2.VideoCapture(video_src)
        self.frame = self.cam.read()

    def run(self):
        while True:
            #mpPose
            success, img = self.cam.read()
            imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            results = pose.process(imgRGB)
            #print(results.pose_landmarks)
            if results.pose_landmarks:
                mpDraw.draw_landmarks(img, results.pose_landmarks, mpPose.POSE_CONNECTIONS)
                for id, lm in enumerate(results.pose_landmarks.landmark):
                    h, w,c = img.shape
                    #print("ID:",id,"/n",lm)
                    #id chosen based off of pose tracking landmark image. (./pose_tracking_full_body_landmarks.png)
                    #...0 = nose.
                    if id == 0:
                        print((results.pose_landmarks.landmark[id]))
                        b2= bytes(str( (results.pose_landmarks.landmark[id]) ),encoding='utf-8')
                        sock.sendto(b2,(UDP_IP,UDP_PORT))
                    ##################################################################################
                        #b2= bytes(str(results.pose_landmarks.landmark[20].x*1000),encoding='utf-8')
                        #sock.sendto(b2,(UDP_IP,UDP_PORT))
                    ##################################################################################

            cTime = time.time()
            fps = 1/(cTime-0)
 
            cv2.putText(img, str(int(fps)), (50,50), cv2.FONT_HERSHEY_SIMPLEX,1,(255,0,0), 3)
            cv2.imshow("Pose Tracking", img)
            cv2.waitKey(1)
        cv2.destroyAllWindows()

if __name__ == '__main__':
    import sys
    try: video_src = sys.argv[1]
    #Changed video_src based off of webcam originally the value was 0.
    except: video_src = 1
    print ("sys.agrv: ", sys.argv, len(sys.argv))
    print ("sys.__doc__: ", __doc__)
    print (video_src)
    App(video_src).run()
