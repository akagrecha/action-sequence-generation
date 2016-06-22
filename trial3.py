import cv2
import numpy as np
import argparse


def action_sequence_generator(video, frames_required=8):
    cap = cv2.VideoCapture(video)
    number_of_frames = int(cap.get(7))
    frame_numbers = [i for i in range(0, number_of_frames-1, int((number_of_frames-1)/frames_required))]
    video_frames = []

    while 1:
        ret, frame = cap.read()
        if ret == 0:
            break

        video_frames.append(frame)
    cap.release()

    first_frame = cv2.cvtColor(video_frames[0], cv2.COLOR_BGR2GRAY)

    width, height = first_frame.shape

    """foreground_final = np.zeros((width, height), np.uint8)
    background_final = np.ones((width, height), np.uint8)
    background_final *= 255

    foreground_final = cv2.cvtColor(foreground_final, cv2.COLOR_GRAY2BGR)
    background_final = cv2.cvtColor(background_final, cv2.COLOR_GRAY2BGR)"""

    foreground_final = None
    background_final = None

    for i in frame_numbers:
        if i == 0:
            continue

        if i == frame_numbers[1]:
            frame = video_frames[i]
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            frame_delta = cv2.absdiff(first_frame, gray)
            fg_mask = cv2.threshold(frame_delta, 50, 255, 0)[1]
            bg_mask = cv2.bitwise_not(fg_mask)

            foreground = cv2.bitwise_and(frame, frame, mask=fg_mask)
            background = cv2.bitwise_and(frame, frame, mask=bg_mask)

            foreground_final = foreground
            background_final = background

        else:
            frame = video_frames[i]
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            frame_delta = cv2.absdiff(first_frame, gray)
            fg_mask = cv2.threshold(frame_delta, 50, 255, 0)[1]
            bg_mask = cv2.bitwise_not(fg_mask)

            foreground = cv2.bitwise_and(frame, frame, mask=fg_mask)
            background = cv2.bitwise_and(frame, frame, mask=bg_mask)

            foreground_final = cv2.bitwise_or(foreground_final, foreground)
            background_final = cv2.bitwise_and(background_final, background)

    result = cv2.bitwise_or(foreground_final, background_final)

    cv2.namedWindow('result', 0)
    cv2.imshow('result', result)
    cv2.waitKey(0) & 0xFF
    cv2.destroyAllWindows()

ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", help="path to the file")
args = vars(ap.parse_args())

if args.get("video") is None:
    print("file not found")

else:
    action_sequence_generator(args["video"])