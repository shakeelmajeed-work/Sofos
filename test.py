#This is the file for all of our custom functions
#Write any functions here and import them into main.py so we can access and call them there 

from picamera import PiCamera
from time import sleep
import cv2
import numpy
import picamera.array

camera = PiCamera()
camera.resolution = (2592, 1952)

def capture_image(i):
    stream = picamera.array.PiRGBArray(camera)
    sleep(2)
    camera.capture('/home/astropi/Documents/Sofos/images/image%s.jpg' % i)
    camera.capture(stream, format='bgr', use_video_port=True)
    original = stream.array

    return original
