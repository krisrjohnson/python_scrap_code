#code to run the web-cam, ouptut video file
#Press 'q' to quit live feed

'''
There should be a handler for video source so it can be abstracted all the way to Webcam, Raspberry Pi, iPhone, etc
Example: https://www.pyimagesearch.com/2016/01/04/unifying-picamera-and-cv2-videocapture-into-a-single-class-with-opencv/
Even better: https://www.pyimagesearch.com/2015/06/01/home-surveillance-and-motion-detection-with-the-raspberry-pi-python-and-opencv/

relevant doc: https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_gui/py_video_display/py_video_display.html
'''


import argparse #not really necessary but for practice
from imutils.video import FPS, WebcamVideoStream
import imutils
import time 
import cv2
import datetime
import numpy as np
import os

#TODO: switch to JSON config file
parser = argparse.ArgumentParser()
parser.add_argument('-o', '--output', dest='output', type=str, default='video_raw_capt.mp4v', help='output vicdeo filepath')
parser.add_argument('-fr', '--frames', dest='frames', type=int, default=20, help='number of frames to capture (running 16 fps)')
parser.add_argument('-src', '--source', dest='video_source', type=int, default=0, help='Device index of the camera')
parser.add_argument('-os', '--operatiing-system', dest='os', type=str, default='win', help='OS needed to properly encode video')
args = vars(parser.parse_args())

print("[INFO] starting video stream...")
stream = cv2.VideoCapture(args['video_source']) 	#stream object has 16 vars, stream.get(3) is W, .get(4) is H
time.sleep(2.0) #let webcam warmup

FPS = int(stream.get(5))
size = (int(stream.get(3)),
        int(stream.get(4)))

#https://gist.github.com/takuma7/44f9ecb028ff00e2132e
if (args['os'] == 'mac'):
	fourcc = cv2.VideoWriter_fourcc('M','J','P','G')
else: 
	fourcc = cv2.VideoWriter_fourcc('H','2','6','4') #mp4v for windows
out = cv2.VideoWriter(args['output'], fourcc, FPS, size, True)

print(size) 	#640x480 on windows, 1280x720 on mac desktop!

'''
	Following while loop checks if an img was captured, if not it exits. 
	If so, iterator incremented and img is added to out(cv2.VideoWriter object)
	If keypress of q, exit
'''

frame_iterator = 0
while (frame_iterator < args['frames']):
	
	ret, frame = stream.read()

	if ret==True:
		print('still going ' + str(frame_iterator))
		frame_iterator += 1
		out.write(frame)
		cv2.imshow('frame',frame)

		if cv2.waitKey(1) & 0xFF == ord('q'):
			break
	else:
		break
	

#cleanup
print("[INFO] Shutting down")
stream.release()
out.release()
cv2.destroyAllWindows()

