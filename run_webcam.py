#code to run the web-cam
#Press 'q' to quit live feed


import argparse #not really necessary but for practice
from imutils.video import VideoStream
import imutils
import time 
import cv2

MAX_WIDTH = 400

parser = argparse.ArgumentParser()
parser.add_argument('-src', '--source', dest='video_source', type=int, default=0, help='Device index of the camera')
parser.add_argument('-o', '--output', dest='destination', type=str, default='video_raw_capt.mp4', help='destination filepath')
args = vars(parser.parse_args())


print("[INFO] camera sensor warming up")

#what's the diff b/t VideoStream and VideoCapture
vs = VideoStream(src=args["video_source"]).start()

time.sleep(2.0) #let camera warm up

while True: 
	frame = vs.read()
	frame = imutils.resize(frame, width=MAX_WIDTH)
	
	cv2.imshow("Frame", frame)
	key = cv2.waitKey(1) & 0xFF

	if key == ord("q"):
		break


print("[INFO] Shutting down")
cv2.destroyAllWindows()
vs.stop()
