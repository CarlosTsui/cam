import cv2
import numpy as np 
import time

cap=cv2.VideoCapture(1)
cv2.namedWindow("test")
cv2.namedWindow("new")
success,frame=cap.read()
bkg=frame
fnt=frame
graybkg=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
grayfnt=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
while success:
	time.sleep(0.01)
	success,frame=cap.read()

	rad=5		#radius of Gaussian blur must be odd
	grayframe=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
	grayframe=cv2.GaussianBlur(grayframe, (rad,rad), 0)

	#grayfnt=cv2.absdiff(grayframe,graybkg)
	#grayfnt=grayframe-graybkg

	bkg=frame
	graybkg=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
	(minval,maxval,minloc,maxloc)=cv2.minMaxLoc(grayframe)
	cv2.circle(frame,maxloc,rad,(255,0,0),2)
	cv2.circle(grayframe,maxloc,rad,(255,0,0),2)

	cv2.imshow("test",frame)
	cv2.imshow("new",grayframe)
	print(maxloc)

	key=cv2.waitKey(1)
	c = chr(key & 255)
	if c in ['q', 'Q', chr(27)]:
		break
cv2.destroyWindow("test")

