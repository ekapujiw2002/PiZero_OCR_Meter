#Applying adaptive thresholding  with parameters:85 and 7

import cv2
import numpy as np
import sys


# read the experimental image
img = cv2.imread(sys.argv[1], 0)
try:
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
except: #For whem a grayscale image is fed
    gray = img.copy() 

if(len(sys.argv) == 4):
    block_size= int(sys.argv[2])
    c = int(sys.argv[3])
else:
    block_size = 85
    c= 7
imgThresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C,
         cv2.THRESH_BINARY_INV, block_size,c)
# display images
cv2.imshow('original', img)
cv2.imshow('imgThresh', imgThresh)
k = cv2.waitKey() & 0xFF

print("Writing image to disk")
cv2.imwrite(sys.argv[1]+"-threshHolded.png",imgThresh)

cv2.destroyAllWindows()
