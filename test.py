#This is the file for all of our custom functions
#Write any functions here and import them into main.py so we can access and call them there 

from picamera import PiCamera
from time import sleep
import cv2
import numpy as np
import picamera.array
from orbit import ISS
import reverse_geocoder

camera = PiCamera()
camera.resolution = (2592, 1952)



def capture_image(i):
    stream = picamera.array.PiRGBArray(camera)
    sleep(2)
    camera.capture('/home/astropi/Documents/Sofos/images/image%s.jpg' % i)

    image = ('/home/astropi/Documents/Sofos/images/image%s.jpg' % i)

    camera.capture(stream, format='bgr', use_video_port=True)
    original = stream.array
    calcpercentage()
    print(original)
    #manipulate_image(image)
    

    

    return original

#function takes in image path and reads it in, resizes it and gets array from it 
def manipulate_image(image):
    img = cv2.imread(image)
    print(img)
    img = np.array(image, dtype=float)/float(255) #NOT WORKING 
    


def coordinates():
    f = open('data.csv','w')
    location = ISS.coordinates() #object
    
    coordinate_pair = (location.latitude.degrees, location.longitude.degrees)
    nearest_city = reverse_geocoder.search(coordinate_pair) #object with data of the nearest city to ISS coordinates

    row = str(coordinate_pair[0])+','+str(coordinate_pair[1])+','+nearest_city[0]["name"]

    f.write(row)
    f.close()

def calcpercentage():
    img = cv2.imread('/home/astropi/Documents/Sofos/images/image1.jpg')
    green = [130, 158, 0]
    diff = 20

    bounds = [([green[2], green[1]-diff, green[0]-diff], [green[2]+diff, green[1]+diff, green[0]+diff])]

    for (low, high) in bounds:
        low = np.array(low)
        high = np.array(high)

        mask = cv2.inRange(img, low, high)
        cv2.imshow("binary mask", mask)
        cv2.waitKey(0)
        output = cv2.bitwise_and(img, img, mask=mask)

        percentage_green = ((cv2.countNonZero(mask))/(img.size)) * 100
        print(str(percentage_green))

