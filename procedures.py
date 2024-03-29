#This is the file for all of our custom functions
#Write any functions here and import them into main.py so we can access and call them there 

from picamera import PiCamera
from time import sleep
import cv2
import numpy as np
import picamera.array
from orbit import ISS
import reverse_geocoder
from fastiecm import fastiecm
import csv

camera = PiCamera()
camera.resolution = (2592, 1952)

def writedata(percent):
    location = ISS.coordinates()
    coordinate_pair = (location.latitude.degrees, location.longitude.degrees)
    nearest_city = reverse_geocoder.search(coordinate_pair)
    with open('data.csv', 'w') as f:
        writer = csv.writer(f)
        data = [percent,coordinate_pair,nearest_city[0]["name"]]
        writer.writerow(data)



def capture_image(i):
    stream = picamera.array.PiRGBArray(camera)
    sleep(2)
    camera.capture('images/image%s.jpg' % i)

    image = ('images/image%s.jpg' % i)

def display(image, image_name): #use as reference for when we want to see what we are doing to an image
    image = np.array(image, dtype=float)/float(255) #remember to convert values within since these are floats
    shape = image.shape
    height = int(shape[0] / 2)
    width = int(shape[1] / 2)
    image = cv2.resize(image, (width, height))

def contrast_stretch(image): #to calculate NDVI need to increase contrast of images
    in_min = np.percentile(image, 5)
    in_max = np.percentile(image, 95)

    out_min = 0.0
    out_max = 255.0

    out = image - in_min
    out *= ((out_min - out_max) / (in_min - in_max))
    out += in_min

    return out

def calc_ndvi(image):
    b, g, r = cv2.split(image)
    bottom = (r.astype(float) + b.astype(float))
    bottom[bottom==0] = 0.01
    ndvi = (b.astype(float) - r) / bottom
    return ndvi

def convert_colourscale(contrasted_image, i):
    color_mapped_prep = contrasted_image.astype(np.uint8)
    color_mapped_image = cv2.applyColorMap(color_mapped_prep, fastiecm)
    cv2.imwrite('images/image%s.jpg' % i, color_mapped_image)

def proportion_vegetation(directory):
    img = cv2.imread(directory) #load in NDVI colourscaled image

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    lower_bound = np.array([36,0,0])
    upper_bound = np.array([86,255,255])

    mask = cv2.inRange(hsv, lower_bound, upper_bound) #create a mask that looks for all green coloured pixels (represent NDVI value above 0.5 which is what we require)

    #result = cv2.bitwise_and(img, img, mask = mask) #for reference

    percent = (cv2.countNonZero(mask)/(2592*1952)) * 100 #find proportion of white pixels (white pixels are pixels from original NDVI image that make it through the mask)
    return percent
