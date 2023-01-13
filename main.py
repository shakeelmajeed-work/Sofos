#Sofos code
from datetime import datetime,timedelta
from test import *

#first thing that will be run is this main function
def main():
    print("Hello Astro-Pi")
    #import the functions from custom_functions.py and call them here in turn  

if __name__ == "__main__":
    start_time = datetime.now()
    now_time = datetime.now()

    run_time = (0.1) #-10 mins for now until we assess how long one round of our code will take because we need to stop our code before the 3 hours is up

    i = 0

    #make program run for 2 hours 50 mins for now
    while (now_time < start_time + timedelta(minutes=run_time)):
        #main()
        i = i+1
        capture_image(i)
        # Update the current time
        now_time = datetime.now()
