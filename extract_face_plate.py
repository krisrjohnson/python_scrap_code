import os
import cv2
import dlib
import time
import argparse
import numpy as np
from imutils import video

DOWNSAMPLE_RATIO = 4
ORIGIN_DIR = 'original'
DEST_DIR = 'faceplate'

def reshape_for_polyline(array):
    return np.array(array, np.int32).reshape((-1, 1, 2))


def main():
    os.makedirs(ORIGIN_DIR, exist_ok=True)
    os.makedirs(DEST_DIR, exist_ok=True)

    cap = cv2.VideoCapture(args.filename)
    fps = video.FPS().start()

    count = 0
    while cap.isOpened():
        ret, frame = cap.read()

        frame_resize = cv2.resize(frame, None, fx=1 / DOWNSAMPLE_RATIO, fy=1 / DOWNSAMPLE_RATIO)
        gray = cv2.cvtColor(frame_resize, cv2.COLOR_BGR2GRAY)
        faces = detector(gray, 1)
        black_image = np.zeros(frame.shape, np.uint8)

        t = time.time()

        # Perform if there is a face detected
        if len(faces) == 1:
            for face in faces:
                detected_landmarks = predictor(gray, face).parts()
                landmarks = [[p.x * DOWNSAMPLE_RATIO, p.y * DOWNSAMPLE_RATIO] for p in detected_landmarks]

                jaw = reshape_for_polyline(landmarks[0:17])
                uni_eyebrow = reshape_for_polyline(landmarks[17:27])
                right_jaw_to_eyebrow = reshape_for_polyline([landmarks[0],landmarks[17]])
                left_jaw_to_eyebrow = reshape_for_polyline([landmarks[16], landmarks[26]])

                #create polygon of bounding points for face shield - 0:16,26:17,0
                face_shield_landmark_list = landmarks[0:17]
                face_shield_landmark_list.append(landmarks[26])
                for i in range(25, 16, -1): face_shield_landmark_list.append(landmarks[i]) #double check range ends before last item
                face_shield_landmark_list.append(landmarks[0])

                color = (255, 255, 255)
                thickness = 1

                '''
                    Jaw is dots 0:16, 
                    connect 0-17 to link upper right jaw to upper right eyebrow
                    right eyebrow is dots 17:21
                    left eyebrow is dots 22:26
                    combined eyebrow is 17:26
                    connect 16-26 to connect upper left jaw to upper left eyebrow
                    TODO: Currently Grabs from MID-EYEBROW! Need to grab the faceplate, so mid-forehead
                '''
                cv2.polylines(black_image, [jaw], False, color, thickness)
                cv2.polylines(black_image, [uni_eyebrow], False, color, thickness)
                cv2.polylines(black_image, [right_jaw_to_eyebrow], False, color, thickness)

                #so now black image should have white pixels defining the face polygon
                cv2.fillPoly(black_image, [jaw, left_jaw_to_eyebrow, uni_eyebrow, right_jaw_to_eyebrow], color, thickness)



            # Display the resulting frame
            count += 1
            print(count)
            cv2.imwrite(f"{ORIGIN_DIR}/{count}.png", frame)
            cv2.imwrite(f"{DEST_DIR}/{count}.png", black_image)
            fps.update()

            print('[INFO] elapsed time: {:.2f}'.format(time.time() - t))

            if count == args.number:  # only take 400 photos
                break
            elif cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            print("No face detected")

    fps.stop()
    print('[INFO] elapsed time (total): {:.2f}'.format(fps.elapsed()))
    print('[INFO] approx. FPS: {:.2f}'.format(fps.fps()))

    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--file', dest='filename', type=str, help='Name of the video file.')
    parser.add_argument('--num', dest='number', type=int, help='Number of train data to be created.')
    parser.add_argument('--landmark-model', dest='face_landmark_shape_file', type=str, help='Face landmark model file.')
    args = parser.parse_args()

    # Create the face predictor and landmark predictor
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor(args.face_landmark_shape_file)

    main()
