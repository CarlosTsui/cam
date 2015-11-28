import cv2
import numpy as np
import serial
import time
import math

pi=3.14159265358979723846
ags=[0 for x in range(0,20)]        #angle_sin
agc=[0 for x in range(0,20)]        #angle_cos
agh=[0 for x in range(0,20)]
angle=22.5
for i in range(1,9):
    agh[i]=2*pi*angle/360
    ags[i]=math.sin(agh[i])
    agc[i]=math.cos(agh[i])
    print(i,angle,agh[i],agc[i])
    angle+=45;

ser = serial.Serial('COM9', 9600)
ser.write("sssssssss")
cv2.namedWindow("test")
cap=cv2.VideoCapture(1)
success, frame = cap.read()
color = (0,0,0)
classfier=cv2.CascadeClassifier("haarcascade_frontalface_alt.xml")
while success:
    #time.sleep(0.01)

    success, frame = cap.read()
    size=frame.shape[:2]
    image=np.zeros(size,dtype=np.float16)
    image = cv2.cvtColor(frame, cv2.cv.CV_BGR2GRAY)
    cv2.equalizeHist(image, image)

    divisor=8
    h, w = size
    minSize=(w/divisor, h/divisor)
    faceRects = classfier.detectMultiScale(image, 1.2, 2, cv2.CASCADE_SCALE_IMAGE,minSize)
    
    #print(len(faceRects))

    if len(faceRects)>0:
        for faceRect in faceRects:
                x, y, w, h = faceRect
                cv2.rectangle(frame, (x, y), (x+w, y+h), color)
                cx=x+(w/2)-320
                cy=-(y+(h/2)-240)
                cz=math.sqrt(cx*cx+cy*cy)
                angle_cos=cy/cz
                angle_sin=cx/cz
                print(x,x+w,y,y+h,"   ",cx,cy,angle_sin,angle_cos)
                #640x480    center:320,240

                if((abs(cx)>10)and(abs(cy)>10)):
                    if(angle_sin>0):        #AQWED
                        if(angle_cos>agc[1]):           #D
                            ser.write("sw")
                        elif(angle_cos>agc[2]):      #E
                            ser.write("se")
                        elif(angle_cos>agc[3]):      #W
                            ser.write("sd")
                        elif(angle_cos>agc[4]):      #Q
                            ser.write("sc")
                        else:                           #A
                            ser.write("sx")
                    elif(angle_sin<=0):
                        if(angle_cos>agc[8]):           #D
                            ser.write("sw")
                        elif(angle_cos>agc[7]):      #C
                            ser.write("sq")
                        elif(angle_cos>agc[6]):      #X
                            ser.write("sa")
                        elif(angle_cos>agc[5]):      #Z
                            ser.write("sz")
                        else:                           #A
                            ser.write("sx")

    cv2.imshow("test", frame)
    key=cv2.waitKey(10)
    c = chr(key & 255)
    if c in ['q', 'Q', chr(27)]:
        break
cv2.destroyWindow("test")
