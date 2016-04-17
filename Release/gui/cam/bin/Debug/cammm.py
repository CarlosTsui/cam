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
import sys

def rec_audio(stat,filename,queue):
	NUM_SAMPLES = 200
	SAMPLING_RATE = 8000
	pa = PyAudio()
	stream = pa.open(format=paInt16, channels=1, rate=SAMPLING_RATE, input=True, frames_per_buffer=NUM_SAMPLES)
	save_count = 0 
	save_buffer = [] 

	while True:
		signal=queue.get()
		if(signal=="audio_start"):
			break

	time_start=clock()

	while True:
		string_audio_data = stream.read(NUM_SAMPLES)
		save_buffer.append( string_audio_data )
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
	queue.put("wav_sav_ok")

def rec_video(stat,framecnt,filename,queue,cap_no):
    framelist=[]
    cap=cv2.VideoCapture(cap_no)
    capsize = (int(cap.get(cv2.cv.CV_CAP_PROP_FRAME_WIDTH)),int(cap.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT)))
    fourcc = cv2.cv.CV_FOURCC('M','S','V','C')
    cv2.namedWindow("test")
    framecnt.value=0
    success, frame = cap.read()
    cv2.imwrite("./temp_frame/0.jpg",frame)
    framelist.append("./temp_frame/0.jpg")
    framecnt.value+=1
    queue.put("rotate_start")
    queue.put("audio_start")
    time_start=clock()

    while True:
        success, frame = cap.read()
        cv2.imwrite("./temp_frame/"+str(framecnt.value)+".jpg",frame)
        framelist.append("./temp_frame/"+str(framecnt.value)+".jpg")
        framecnt.value+=1
        cv2.imshow("test", frame)
        
        #print(frame.shape)
        #print(type(frame))

        key=cv2.waitKey(10)
        c = chr(key & 255)
        if c in ['q', 'Q', chr(27)]:
            time_finish=clock()
            #with stat.get_lock()
            stat.value = 1
            break

    cap.release()
    cv2.destroyAllWindows()

    while True:
    	signal=queue.get()
    	if(signal=="wav_sav_ok"):
    		print("wav_completed")
    		break

   	print("video_start: "+str(time_start))
    print("video_end: "+str(time_finish))
    print("video_duration (sec): "+str(time_finish-time_start))   #duration (second)
    print("total frames: "+str(framecnt.value))
    cvfps=framecnt.value/(time_finish-time_start)
    print("fps: "+str(cvfps))                               #fps

    clip=ImageSequenceClip(framelist,fps=cvfps)
    audio_clip=AudioFileClip("./temp_frame/"+filename+".wav")
    sndclip=clip.set_audio(audio_clip)
    sndclip.to_videofile("./"+filename+".mp4",fps=cvfps)

def engine_rotating(stat,framecnt,queue):
	classfier=cv2.CascadeClassifier("D:\\Anaconda\\haarcascade_frontalface_alt.xml")
	color = (255,0,0)
	while True:
		signal=queue.get()
		if(signal=="rotate_start"):
			break

	print("eng_start")

	while True:
		if(stat.value==1):
			break
		cnt=framecnt.value-1
		frame=cv2.imread("./temp_frame/"+str(cnt)+".jpg")
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
				print("detected face: ",x,y,w,h)
				#cv2.rectangle(frame, (x, y), (x+w, y+h), color)
				#TODO: Please Code Here

	print("rotating finish")

if __name__=='__main__':
	recording_status=mulp.Value('i',0)
	recording_cnt=mulp.Value('i',0)
	filename = datetime.now().strftime("%Y-%m-%d_%H_%M_%S")

	_cap_no=int(sys.argv[1])
	#cap_no=mulp.Value('i',_cap_no)

	queue = mulp.Queue(3)
	p1=mulp.Process(target=rec_audio,args=(recording_status,filename,queue,))
	p2=mulp.Process(target=rec_video,args=(recording_status,recording_cnt,filename,queue,_cap_no,))
	p3=mulp.Process(target=engine_rotating,args=(recording_status,recording_cnt,queue,))
	p1.start()
	p2.start()
	p3.start()
	p1.join()
	p2.join()
	p3.join()
	queue.close()


