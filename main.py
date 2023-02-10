#Sofos code
from datetime import datetime,timedelta
from procedures import *


'''data.csv format:
    current coordinates
    nearest city 
    relative percentage area of live green vegetation in the image
'''
header = ['Percentage of live green vegetation in the image', 'Coordinate Pair', 'Nearest City']
with open('data.csv', 'w') as f:
    writer = csv.writer(f)
    writer.writerow(header)

def main():
    print("Hello Astro-Pi")

if __name__ == "__main__":
    start_time = datetime.now()
    now_time = datetime.now()

    run_time = (178)

    i = 0

    #make program run for 2 hours 50 mins for now
    while (now_time < start_time + timedelta(minutes=run_time)):
        try:
            i = i+1
            capture_image(i)
            directory = "images/image%s.jpg" % i

            image = cv2.imread(directory)
            contrasted = contrast_stretch(image)
            ndvi = calc_ndvi(contrasted)
            ndvi_contrasted = contrast_stretch(ndvi) #in greyscale which is hard for us to decipher
            convert_colourscale(ndvi_contrasted, i)


            percent = proportion_vegetation(directory)
            writedata(percent)

            # Update the current time
            now_time = datetime.now()
        except:
            continue
