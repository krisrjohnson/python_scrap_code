#python generate_train_data.py --file angela_merkel_speech.mp4 --num 400 --landmark-model shape_predictor_68_face_landmarks.dat

'''
    Original file was 'generate_train_data.py' from github.com/datitran/face2face-demo
    cmd for that file: python generate_train_data.py --file some_video.mp4 --num 400 --landmark-model shape_predictor_68_face_landmarks.dat

    this file takes a video and split it, with an option for max num of frames
    would additionally like the option to do landmarking in this file
        would involve user supplying a landmark.dat file for the model
        and bringing in a landmarking method based on the og generate_train_data.py landmark fn
        og landmark:
            created landmark directory
            detected face
            if face, created downsized landmark frame
            drew polylines based on landmarks
            wrote landmark_frame to landmark dir

'''

import os   #for making directories
import cv2  #for VideoCapture and video methods
import time     #for timestamping
import argparse     #for handling CLI args
import numpy as np  #for handling img dataframes
from imutils import video   #not sure....



def reshape_for_polyline(array):
    return np.array(array, np.int32).reshape((-1, 1, 2))


def main():
    os.makedirs('original', exist_ok=True)

    cap = cv2.VideoCapture(args.filename)
    fps = video.FPS().start()

    count = 0
    while cap.isOpened():
        ret, frame = cap.read()
        t = time.time()

        if ret is True:
            # Display the resulting frame
            count += 1
            print(count)
            cv2.imwrite("original/{}.png".format(count), frame)
            fps.update()

            print('[INFO] elapsed time: {:.2f}'.format(time.time() - t))

            if count == args.number:  # only take 400 photos
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


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--file', dest='filename', type=str, help='Name of the video file.')
    parser.add_argument('--num', dest='number', type=int, help='Number of train data to be created.')
    args = parser.parse_args()

    main()
