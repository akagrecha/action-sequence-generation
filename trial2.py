import cv2
import argparse
import datetime
import time

ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", help = "path to the video file")
# ap.add_argument("-a", "--min-area", type=int, default=500, help="minimum area size")
args = vars(ap.parse_args())

if args.get("video") is None:
	print("file not found")
	
else:
	cap = cv2.VideoCapture(args["video"])
	frames = int(cap.get(7))
	
	firstFrame = None

	img_fg = []
	img_bg = []

	while(1):
		ret, frame = cap.read()

		if ret == 0:
			break

		gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		gray = cv2.GaussianBlur(gray, (21,21), 0)

		if firstFrame == None:
			firstFrame = gray
			continue

		frameDelta = cv2.absdiff(firstFrame, gray)
		fgmask = cv2.threshold(frameDelta, 50, 255, 0)[1]
		bgmask = cv2.bitwise_not(fgmask)
		
		foreground = cv2.bitwise_and(frame, frame, mask = fgmask)
		background = cv2.bitwise_and(frame, frame, mask = bgmask)

		img_fg.append(foreground)
		img_bg.append(background)

		cv2.namedWindow('original', 0)
		cv2.namedWindow('background', 0)
		cv2.namedWindow('foreground', 0)

		cv2.imshow('original', frame)
		cv2.imshow('background', background)
		cv2.imshow('foreground', foreground)

		k = cv2.waitKey(50) & 0xFF
		if k == 27:
			break

	cap.release()
	cv2.destroyAllWindows()
	
	frame_no = [i for i in range(0, frames, int(frames/6))]
	foreground = img_fg[0]
	background = img_bg[0]
	for i in frame_no:
		foreground = cv2.bitwise_or(img_fg[i], foreground)
		background = cv2.bitwise_and(img_bg[i], background)
	
	result = cv2.bitwise_or(foreground, background)
	
	cv2.namedWindow('background', 0)
	cv2.namedWindow('foreground', 0)
	cv2.namedWindow('result', 0)
	
	cv2.imshow('foreground', foreground)
	cv2.imshow('background', background)
	cv2.imshow('result', result)
	
	k = cv2.waitKey(0) & 0xFF
	
	cv2.destroyAllWindows()
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	


	
	
	
	
	
	
	
	
	
	
