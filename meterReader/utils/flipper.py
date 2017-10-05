import cv2
import sys
#Flip black and white in a grayscale image
#Overwrites the image
def flipper(imgString):
     img = cv2.imread(imgString)
     img = cv2.bitwise_not(img)
     cv2.imwrite(imgString,img)


flipper(sys.argv[1])
