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

ser = serial.Serial('COM4', 115200)
ser.write("sssssssss")
cv2.namedWindow("test")
cap=cv2.VideoCapture(1)
success, frame = cap.read()     
color = (0,0,111)
classfier=cv2.CascadeClassifier("D:\\HFUTProject\\cam\\cam_Controller_Py\\haarcascade_frontalface_alt.xml")  
while success:
    time.sleep(0.05	)

    success, frame = cap.read()
    size=frame.shape[:2]       
    image=np.zeros(size,dtype=np.float16)   
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  
    cv2.equalizeHist(image, image)  

    divisor=16
    h, w = size
    minSize=(w/divisor, h/divisor)
    faceRects = classfier.detectMultiScale(image, 1.2, 2, cv2.CASCADE_SCALE_IMAGE,minSize)
    
    print(len(faceRects))

    if len(faceRects)>0:
        for faceRect in faceRects:
                x, y, w, h = faceRect
                cv2.rectangle(frame, (x, y), (x+w, y+h), color,3)
                cx=x+(w/2)-320
                cy=-(y+(h/2)-240)
                cz=math.sqrt(cx*cx+cy*cy)
                angle_cos=cy/cz
                angle_sin=cx/cz
                #640x480    center:320,240

                if((abs(cx)>100)or(abs(cy)>75)):
                    print(x,x+w,y,y+h,"   ",cx,cy,angle_sin,angle_cos)
                    if(angle_sin>0):        #AQWED
                        if(angle_cos>agc[1]):           #D
                            ser.write("sww")
                        elif(angle_cos>agc[2]):      #E
                            ser.write("see")
                        elif(angle_cos>agc[3]):      #W
                            ser.write("sddd")
                        elif(angle_cos>agc[4]):      #Q
                            ser.write("scc")
                        else:                           #A
                            ser.write("sxx")
                    elif(angle_sin<=0):
                        if(angle_cos>agc[8]):           #D
                            ser.write("sww")
                        elif(angle_cos>agc[7]):      #C
                            ser.write("sqq")
                        elif(angle_cos>agc[6]):      #X
                            ser.write("saaa")
                        elif(angle_cos>agc[5]):      #Z
                            ser.write("szz")
                        else:                           #A
                            ser.write("sxx")
                elif((abs(cx)>40)or(abs(cy)>30)):
                    print(x,x+w,y,y+h,"   ",cx,cy,angle_sin,angle_cos)
                    if(angle_sin>0):        #AQWED
                        if(angle_cos>agc[1]):           #D
                            ser.write("sw")
                        elif(angle_cos>agc[2]):      #E
                            ser.write("se")
                        elif(angle_cos>agc[3]):      #W
                            ser.write("sdd")
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
                            ser.write("saa")
                        elif(angle_cos>agc[5]):      #Z
                            ser.write("sz")
                        else:                           #A
                            ser.write("sx")

    cv2.imshow("test", frame)
    key=cv2.waitKey(1)
    c = chr(key & 255)
    if c in ['q', 'Q', chr(27)]:
        break
cv2.destroyWindow("test")
