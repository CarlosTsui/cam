import cv2
import numpy as np
from time import clock
from moviepy.editor import *
import os
import shutil
from pyaudio import PyAudio, paInt16 
from datetime import datetime 
import wave
import multiprocessing as mulp
import scipy.io as sio

def rec_audio(stat,filename,pipe):
	NUM_SAMPLES = 2000
	SAMPLING_RATE = 8000
	LEVEL = 1500
	COUNT_NUM = 20
	SAVE_LENGTH = 8
	pa = PyAudio()
	stream = pa.open(format=paInt16, channels=1, rate=SAMPLING_RATE, input=True, frames_per_buffer=NUM_SAMPLES)
	save_count = 0 
	save_buffer = [] 
	time_start=clock()

	while True:
		string_audio_data = stream.read(NUM_SAMPLES)
		save_buffer.append( string_audio_data )
		#signal=pipe.recv()			#bug: blocked while cannot recv signal
		#if(signal=="rec_ter"):		#terminate
		if(stat.value==1):
			break

	time_finish=clock()
	wf = wave.open("./temp_frame/"+filename+".wav", 'wb') 
	wf.setnchannels(1) 
	wf.setsampwidth(2) 
	wf.setframerate(SAMPLING_RATE) 
	wf.writeframes("".join(save_buffer)) 
	wf.close() 
	save_buffer = [] 

	print("audio_start: "+str(time_start))
	print("audio_end: "+str(time_finish))
	print("audio_duration (sec): "+str(time_finish-time_start))   #duration (second)
	print ("audio_file: ", filename, "saved" )
	pipe.send("wav_sav_ok")

def rec_video(stat,filename,pipe):
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

    while True:
        framecnt+=1
        success, frame = cap.read()
        #cv2.imwrite("./temp_frame/"+str(framecnt)+".jpg",frame)
        #framelist.append("./temp_frame/"+str(framecnt)+".jpg")
        #cv2.imshow("test", frame)
        
        #print(frame.shape)
        #print(type(frame))

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
            #pipe.send("rec_ter")
            #with stat.get_lock()
            stat.value = 1
            break

    cap.release()
    cv2.destroyAllWindows()

    while True:
    	signal=pipe.recv()
    	if(signal=="wav_sav_ok"):
    		break
   	print("video_start: "+str(time_start))
    print("video_end: "+str(time_finish))
    print("video_duration (sec): "+str(time_finish-time_start))   #duration (second)
    print("total frames: "+str(framecnt))
    cvfps=framecnt/(time_finish-time_start)
    print("fps: "+str(cvfps))                               #fps

    clip=ImageSequenceClip(framelist,fps=cvfps)
    audio_clip=AudioFileClip("./temp_frame/"+filename+".wav")
    sndclip=clip.set_audio(audio_clip)
    sndclip.to_videofile("./"+filename+".mp4",fps=cvfps)

if __name__=='__main__':
	recording_status=mulp.Value('i',0)
	filename = datetime.now().strftime("%Y-%m-%d_%H_%M_%S")
	#pool=mulp.Pool(processes=2)
	pipe=mulp.Pipe()
	p1=mulp.Process(target=rec_audio,args=(recording_status,filename,pipe[0],))
	p2=mulp.Process(target=rec_video,args=(recording_status,filename,pipe[1],))
	p1.start()
	p2.start()
	p1.join()
	p2.join()




