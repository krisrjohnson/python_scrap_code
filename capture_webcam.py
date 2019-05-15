#code to run the web-cam
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

MAX_WIDTH = 400

parser = argparse.ArgumentParser()
parser.add_argument('-src', '--source', dest='video_source', type=int, default=0, help='Device index of the camera')
parser.add_argument('-o', '--output', dest='output', type=str, default='video_raw_capt.mp4v', help='output vicdeo filepath')
args = vars(parser.parse_args())

print("[INFO] starting video stream...")
#stream = WebCamVideoStream(src=args["video_source"]).start() # 0 is webcam, which is the default
stream = cv2.VideoCapture(args["video_source"]) 	#stream.get(3) is width stream.get(4) is height
time.sleep(2.0) #let webcam warmup

size = (int(stream.get(3)),
        int(stream.get(4)))

#define video codec and create VideoWriter object so can save
#https://gist.github.com/takuma7/44f9ecb028ff00e2132e
fourcc = cv2.VideoWriter_fourcc('M','J','P','G')
#out = cv2.VideoWriter(args["output"], fourcc, 20.0, size, True)
out = cv2.VideoWriter('video_raw_capt.avi', fourcc, 16, size, True)

print(size) 	#1280x720!

'''
	numpy is (row by col)
	img is (width by height)
'''

'''
	Following while loop checks if an img was captured, if not it exits. 
	If so, iterator incremented and img is added to out(cv2.VideoWriter object)
	If keypress of p, pause until another keypress of p
	If keypress of q, exit
'''

frame_iterator = 0
while (frame_iterator < 20):
	
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

