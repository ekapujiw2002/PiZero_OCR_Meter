


import cv2
import numpy as np
import sys

# this function is needed for the createTrackbar step downstream
def nothing(x):
    pass

# read the experimental image
img = cv2.imread(sys.argv[1], 0)

# create trackbar for canny edge detection threshold changes
cv2.namedWindow('canny')

# add ON/OFF switch to "canny"
switch = '0 : OFF \n1 : MEAN_C\n2 : GAUSSIAN_C'
cv2.createTrackbar(switch, 'canny', 0, 2, nothing)

# add lower and upper threshold slidebars to "canny"
cv2.createTrackbar('lower', 'canny', 0, 200, nothing)
cv2.createTrackbar('upper', 'canny', 0, 20, nothing)

# Infinite loop until we hit the escape key on keyboard
while(True):
    a= cv2.waitKey(30)
    # get current positions of four trackbars
    lower = cv2.getTrackbarPos('lower', 'canny')
    upper = cv2.getTrackbarPos('upper', 'canny')
    s = cv2.getTrackbarPos(switch, 'canny')

    if(lower % 2== 0):
        lower+=1
    if s == 0:
        imgThresh = img
    else:
        gray = img.copy() #cv2.cvtColor(img,cv2.COLOR_BGR2GRAY) #Convert to gray
        if(s == 1):
            threshStyle = cv2.ADAPTIVE_THRESH_MEAN_C
        elif(s==2):
            threshStyle = cv2.ADAPTIVE_THRESH_GAUSSIAN_C
        try:
            imgThresh = cv2.adaptiveThreshold(gray, 255, threshStyle ,
             cv2.THRESH_BINARY_INV, lower, upper)
        except:
            print("BAD VALUES, PLEASE ADJUST")
        print("Applying adaptive thresholding  with parameters:"+ str(lower) + " and "+ str(upper))

    # display images
    cv2.imshow('original', img)
    cv2.imshow('imgThresh', imgThresh)
    k = cv2.waitKey(1) & 0xFF
    if k == 27:   # hit escape to quit
        break

cv2.destroyAllWindows()
