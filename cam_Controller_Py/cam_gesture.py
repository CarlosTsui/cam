import cv2
import numpy as np 
import time

cap=cv2.VideoCapture(0)
cv2.namedWindow("test")
#cv2.namedWindow("new")
success,frame=cap.read()
bkg=frame
fnt=frame
graybkg=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
grayfnt=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
vec=[0 for x in range(0,10)]
veccnt=0
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
	if(maxval>150):
		cv2.circle(frame,maxloc,rad,(255,0,0),2)
		cv2.circle(grayframe,maxloc,rad,(255,0,0),2)

		vec[veccnt]=maxloc[0]
		#print(vec[veccnt])
		veccnt+=1
		moved=1
		if(veccnt==10):
			veccnt=0
			for i in range(1,10):
				speed=vec[i]-vec[i-1]
				if(abs(speed)<6):
					moved=0
			if(moved==1):
				if(vec[9]>vec[0]):
					print("right")
				else:
					print("left")

	cv2.imshow("test",frame)
	#cv2.imshow("new",grayframe)
	#print(maxloc,maxloc[0])

	key=cv2.waitKey(1)
	c = chr(key & 255)
	if c in ['q', 'Q', chr(27)]:
		break
cv2.destroyWindow("test")

