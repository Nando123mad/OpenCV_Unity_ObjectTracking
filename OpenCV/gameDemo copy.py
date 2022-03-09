import sys
#Change the following line
sys.path.append('C:\Python310\Lib\site-packages\cv2')

import numpy as np
import cv2

import socket
import time

def testDevice(source):
   cap = cv2.VideoCapture(source) 
   if cap is None or not cap.isOpened():
       print('Warning: unable to open video source: ', source)
   else:
        print('Congrats: opened video source: ', source)

testDevice(0) # no printout
testDevice(1) # prints message