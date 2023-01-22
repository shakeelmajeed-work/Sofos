import cv2
import numpy as np
from fastiecm import fastiecm

#"/home/astropi/Documents/Sofos/images/image1.jpg"

directory = "images/astropi_pinoir.png"
image = cv2.imread(directory)

def display(image, image_name): #use as reference for when we want to see what we are doing to an image
    image = np.array(image, dtype=float)/float(255) #remember to convert values within since these are floats
    shape = image.shape
    height = int(shape[0] / 2)
    width = int(shape[1] / 2)
    image = cv2.resize(image, (width, height))
    cv2.namedWindow(image_name)
    cv2.imshow(image_name, image)
    cv2.waitKey(0) #press 0 to see close
    cv2.destroyAllWindows()

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

def convert_colourscale(contrasted_image):
    color_mapped_prep = contrasted_image.astype(np.uint8)
    color_mapped_image = cv2.applyColorMap(color_mapped_prep, fastiecm)
    display(color_mapped_image, 'Color mapped')


display(image, 'Original')
contrasted = contrast_stretch(image)
display(contrasted, 'Contrasted original') #need to save this
#cv2.imwrite('images/image.jpg', contrasted)
ndvi = calc_ndvi(contrasted)
# display(ndvi, 'NDVI') #would still be dark
ndvi_contrasted = contrast_stretch(ndvi) #in greyscale which is hard for us to decipher
convert_colourscale(ndvi_contrasted)