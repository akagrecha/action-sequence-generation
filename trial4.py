import cv2
import argparse


def action_sequence_generator(video, frames_required=8):

    cap = cv2.VideoCapture(video)
    number_of_frames = int(cap.get(7))
    frame_numbers = [i for i in range(0, number_of_frames - 1, int((number_of_frames - 1) / frames_required))]
    video_frames = []

    while 1:
        ret, frame = cap.read()

        if ret == 0:
            break
        # frame = cv2.GaussianBlur(frame, (7, 7), 0)

        video_frames.append(frame)

    cap.release()

    first_frame = cv2.cvtColor(video_frames[0], cv2.COLOR_BGR2GRAY)
    result = video_frames[0]

    for i in frame_numbers:
        if i == 0:
            continue

        frame = video_frames[i]

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frame_delta = cv2.absdiff(gray, first_frame)
        foreground_mask = cv2.threshold(frame_delta, 35, 255, 0)[1]
        background_mask = cv2.bitwise_not(foreground_mask)

        foreground = cv2.bitwise_and(frame, frame, mask=foreground_mask)

        result = cv2.bitwise_and(result, result, mask=background_mask)
        result = cv2.add(result, foreground)

    cv2.namedWindow('result', 0)
    cv2.imshow('result', result)
    cv2.waitKey(0) & 0xFF
    cv2.destroyAllWindows()

    return result

ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", help="path to the file")
args = vars(ap.parse_args())

if args.get("video") is None:
    print("file not found")

else:
    action_sequence_generator(args["video"], frames_required=8)

