import sys
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
import serial
import time
import math

def welcome(str):
	print(str)

if __name__=='__main__':
	for i in range(1,10000):
		print(i,)
	print(sys.argv[0])
	print(sys.argv[1])
	print(sys.argv[2])
	print(sys.argv[3])
