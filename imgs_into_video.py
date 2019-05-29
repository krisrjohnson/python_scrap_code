import os
import cv2
import numpy as np
import glob
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-o','--output', dest='output_file', type=str, help='Name of the video file to output')
parser.add_argument('-i','--input', dest='input_location', type=str, help='location of input images folder', default='/merkris')
parser.add_argument('-fn','--frames-number', dest='frames_number', type=int, help='number frames to merge into a video', default=None)
parser.add_argument('-os', '--operatiing-system', dest='os', type=str, default='win', help='OS needed to properly encode video')
args = parser.parse_args()


if (args.frames_number == None):
    FRAMES = len(os.listdir(path)) #could be additional files
else:
    FRAMES = args.frames_number
#why build the array of imgs? Just load the img and then add it to cv2.VideoWriter immediately no?

#glob example: for img_name in glob.glob('/Volumes/ThunderQuadX3/HFTF Dropbox/Awesome Freelancer/KJ/gitrepos/PRNet/merkris/*.png'):
img_array = []
for i in range(1, FRAMES+1):
    img_name = f'{args.input_location}/{i}.png'
    print(img_name)
    img = cv2.imread(img_name)
    img_array.append(img)
 
height, width, layers = img.shape
size = (width,height)

if (args['os'] == 'mac'):
	fourcc = cv2.VideoWriter_fourcc('M','J','P','G')
else: 
	fourcc = cv2.VideoWriter_fourcc('H','2','6','4') #mp4v for windows

out = cv2.VideoWriter(f'{args.output_file}.avi', fourcc, 30, size, True)

for i in range(len(img_array)):
    out.write(img_array[i])

cv2.destroyAllWindows()
out.release()