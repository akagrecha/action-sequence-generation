import cv2
import numpy as np

cap = cv2.VideoCapture('dive.mp4')

# background subtractors
fg_ext = cv2.BackgroundSubtractorMOG2()
# number of frames in the video
frames = int(cap.get(7))

# arrays that will contain the frames
img_fg = []
img_bg = []

while 1 :
    ret, frame = cap.read()
    if ret == 0:
        break
        
    # masks
    fg_mask = fg_ext.apply(frame, learningRate = -1)
    bg_mask = cv2.bitwise_not(fg_mask)

    # foreground and background frames
    foreground = cv2.bitwise_and(frame, frame, mask=fg_mask)
    background = cv2.bitwise_and(frame, frame, mask=bg_mask)
    
    # frames added to arrays
    img_fg.append(foreground)
    img_bg.append(background)
    
    cv2.namedWindow('foreground', 0)
    cv2.namedWindow('background', 0)

    cv2.imshow('foreground', foreground)
    cv2.imshow('background', background)

    k = cv2.waitKey(200) & 0xFF
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()

frame_no = [i for i in range(0,frames,6)]
foreground = img_fg[0]
background = img_bg[0]


# operations to generate background and foreground
for i in frame_no:
	foreground = cv2.bitwise_or(foreground, img_fg[i])
	background = cv2.bitwise_and(background, img_bg[i])

# composition of background and foreground
result = cv2.bitwise_or(foreground, background)

cv2.namedWindow('foreground', 0)
cv2.namedWindow('background', 0)
cv2.namedWindow('result', 0)


cv2.imshow('foreground', foreground)
cv2.imshow('background', background)
cv2.imshow('result', result)

k = cv2.waitKey(0) & 0xFF
cv2.destroyAllWindows()











