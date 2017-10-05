import cv2

cam = cv2.VideoCapture(0)

def webcamCapture():    #Get webcam frames
    # cam= cv2.VideoCapture(0) #Initialise camera
    for _ in range(5):
        cam.read()    #Read a few frames at the beginning
    ret,img = cam.read()
    img = cv2.flip(img,1)
    return img.copy()

img = webcamCapture()
cv2.imshow("Webcam capture",img)
cv2.waitKey(10000)
