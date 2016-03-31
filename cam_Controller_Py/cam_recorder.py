# record video and audio seperately
# then combine them by moviepy.set_audio
# ref:
# https://zulko.github.io/moviepy/_modules/moviepy/video/VideoClip.html#VideoClip.set_audio

import cv2
import numpy as np
from time import clock
from moviepy.editor import ImageSequenceClip
import os
import shutil
from pyaudio import PyAudio, paInt16 
from datetime import datetime 
import wave

def rec_video():
    NUM_SAMPLES = 2000
    SAMPLING_RATE = 8000
    LEVEL = 1500
    COUNT_NUM = 20
    SAVE_LENGTH = 8
    pa = PyAudio()
    stream = pa.open(format=paInt16, channels=1, rate=SAMPLING_RATE, input=True, frames_per_buffer=NUM_SAMPLES)
    save_count = 0 
    save_buffer = [] 

    framelist=[]
    cap=cv2.VideoCapture(1)
    capsize = (int(cap.get(cv2.cv.CV_CAP_PROP_FRAME_WIDTH)),int(cap.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT)))
    fourcc = cv2.cv.CV_FOURCC('M','S','V','C')
    time_start=clock()
    cv2.namedWindow("test")
    success, frame = cap.read()
    color = (255,0,0)
    classfier=cv2.CascadeClassifier("D:\\Anaconda\\haarcascade_frontalface_alt.xml")
    framecnt=0
    while success:
        string_audio_data = stream.read(NUM_SAMPLES)
        save_buffer.append( string_audio_data )

        framecnt+=1
        success, frame = cap.read()
        #cv2.imwrite("./temp_frame/"+str(framecnt)+".jpg",frame)
        #framelist.append("./temp_frame/"+str(framecnt)+".jpg")
        #cv2.imshow("test", frame)
        print(frame.shape)
        print(type(frame))

        size=frame.shape[:2]
        image=np.zeros(size,dtype=np.float16)
        image = cv2.cvtColor(frame, cv2.cv.CV_BGR2GRAY)
        cv2.equalizeHist(image, image)
        divisor=32
        h, w = size
        minSize=(w/divisor, h/divisor)
        faceRects = classfier.detectMultiScale(image, 1.2, 2, cv2.CASCADE_SCALE_IMAGE,minSize)
        if len(faceRects)>0:
            for faceRect in faceRects:
                x, y, w, h = faceRect
                cv2.rectangle(frame, (x, y), (x+w, y+h), color)
        cv2.imwrite("./temp_frame/"+str(framecnt)+".jpg",frame)
        framelist.append("./temp_frame/"+str(framecnt)+".jpg")
        cv2.imshow("test", frame)

        key=cv2.waitKey(10)
        c = chr(key & 255)
        if c in ['q', 'Q', chr(27)]:
            time_finish=clock()
            break

    cap.release()
    cv2.destroyAllWindows()

    print(time_start)
    print(time_finish)
    print("duration (sec): "+str(time_finish-time_start))   #duration (second)
    print("total frames: "+str(framecnt))
    cvfps=framecnt/(time_finish-time_start)
    print("fps: "+str(cvfps))                               #fps


    filename = datetime.now().strftime("%Y-%m-%d_%H_%M_%S")
    clip=ImageSequenceClip(framelist,fps=cvfps)
    clip.to_videofile("./"+filename+".mp4",fps=cvfps)

    wf = wave.open(filename+".wav", 'wb') 
    wf.setnchannels(1) 
    wf.setsampwidth(2) 
    wf.setframerate(SAMPLING_RATE) 
    wf.writeframes("".join(save_buffer)) 
    wf.close() 
    save_buffer = [] 
    print filename, "saved" 

if __name__=='__main__':
    rec_video()

