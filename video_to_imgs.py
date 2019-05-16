import os   #for making directories
import cv2  #for VideoCapture and video methods
import time     #for timestamping
import argparse     #for handling CLI args
import numpy as np  #for handling img dataframes
from imutils import video   #not sure....


def main():
    os.makedirs('original', exist_ok=True)

    cap = cv2.VideoCapture(args.filename)
    fps = video.FPS().start()

    frame_count = 0
    image_number = 0
    while cap.isOpened():   #if specified num of frames is too great, this will return false and break the while loop
        ret, frame = cap.read()
        t = time.time()

        if ret is True:
            # Display the resulting frame
            frame_count += 1
            print(frame_count)

            if frame_count >= args.start_frame:
                image_number += 1
                cv2.imwrite(f'{args.output}/{image_number}.png', frame)
            
            fps.update()
            print('[INFO] elapsed time: {:.2f}'.format(time.time() - t))

            if frame_count == (args.number + args.start_frame):  #default is 400
                break
            elif cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            break

    fps.stop()
    print('[INFO] elapsed time (total): {:.2f}'.format(fps.elapsed()))
    print('[INFO] approx. FPS: {:.2f}'.format(fps.fps()))

    cap.release()
    cv2.destroyAllWindows()

#TODO: configs in a json file
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-f','--file', dest='filename', type=str, help='Name of the video file.')
    parser.add_argument('--num', dest='number', default=400, type=int, help='Number of training data frames to be created.')
    parser.add_argument('-o','--output', dest='output', type=str, help='destination folder of output')
    parser.add_argument('-s','--start_frame', dest='start_frame', type=int, default=0, help='starting frame')
    args = parser.parse_args()

    main()
