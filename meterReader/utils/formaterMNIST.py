#Take an image,
#Process it
#Save it as a 28x28 grayscale
import sys
import os
import cv2
import numpy as np


def imageToSample( imgFileName,label,invert = 0):
    #Read img
    imgSource =cv2.imread(imgFileName)
    #Covert to gray
    gray = cv2.cvtColor(imgSource,cv2.COLOR_BGR2GRAY) #Convert to gray
    #Threshold
    imgThresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C,
             cv2.THRESH_BINARY_INV, 51, 10)
    imgThresh = cv2.medianBlur(imgThresh, 3)


    if(invert):
        imgThresh = cv2.bitwise_not(imgThresh)
    cv2.imshow("Result of thresholding",imgThresh)
    #Apply morphological ops
    #kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(10,10))
    #imgThresh = cv2.morphologyEx(imgThresh,cv2.MORPH_CLOSE,kernel)
    
    #Resize to 28x28
    imgSmall = cv2.resize(imgThresh,(28,28), interpolation = cv2.INTER_AREA)

    cv2.imshow(str(label), imgSmall)
    cv2.waitKey()
    #Flatten
    imgsmol = np.ravel(imgSmall)
    #Return with label attached
    cv2.imwrite("processed-"+str(label)+ ".png",imgSmall)
    return (imgsmol,label)

#Use first arg as image
#Use second arg as label
data, label = imageToSample(sys.argv[1],sys.argv[2],1)
print(data)
