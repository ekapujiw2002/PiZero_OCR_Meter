import cv2
import numpy as np
import time
try:
    from picamera.array import PiRGBArray
    from picamera import PiCamera
except:
    print("Picamera import error. Ignore if not usign Pi Camera")

class ImageSource:
    webcamActive = False

    def __init__(self):
        cam = cv2.VideoCapture(0)
        webcamActive = cam.isOpened() 
        if(webcamActive):
            for _ in range(5):
                cam.read()          #Read a few frames at the beginning
        else:
            # initialize the camera and grab a reference to the raw camera capture
            print("Initialising pi camera")
            self.picam = PiCamera()
            self.picam.resolution= (2592,1944)
            self.picam.framerate = 32
            self.rawCapture = PiRGBArray(self.picam, size=(640,480))		

    def webcamCapture(self):    #Get webcam frames
        cam = cv2.VideoCapture(0)
        ret,img = cam.read()
        img = cv2.flip(img,1)
        return img.copy()

    def picamCapture(self):

        # allow the camera to warmup
        #time.sleep(0.1)

        # capture frames from the camera
        self.picam.capture(self.rawCapture,format="bgr")
	# grab the raw NumPy array representing the image, then initialize the timestamp
        # and occupied/unoccupied text
        image = self.rawCapture.array
        # clear the stream in preparation for the next frame
        self.rawCapture.truncate(0)
        return image
'''''
test = ImageSource()
print( "Do we have the webcam opened ? "+ str(test.webcamActive))
while True:
	img = test.picamCapture() 
	cv2.imshow("Test", img)
	cv2.waitKey(1)
'''''
