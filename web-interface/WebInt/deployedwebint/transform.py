#!/home/pi/.virtualenvs/cv/bin/python3
# Use the interpreter in the virtual enviroment with OpenCV bindings
# Probably worth removing virtual enviroments from re-builds
# import the necessary packages
import numpy as np
import cv2
import os
import sys
def order_points(pts):
	# initialzie a list of coordinates that will be ordered
	# such that the first entry in the list is the top-left,
	# the second entry is the top-right, the third is the
	# bottom-right, and the fourth is the bottom-left
	rect = np.zeros((4, 2), dtype = "float32")

	# the top-left point will have the smallest sum, whereas
	# the bottom-right point will have the largest sum
	s = pts.sum(axis = 1)
	rect[0] = pts[np.argmin(s)]
	rect[2] = pts[np.argmax(s)]

	# now, compute the difference between the points, the
	# top-right point will have the smallest difference,
	# whereas the bottom-left will have the largest difference
	diff = np.diff(pts, axis = 1)
	rect[1] = pts[np.argmin(diff)]
	rect[3] = pts[np.argmax(diff)]

	# return the ordered coordinates
	return rect

def four_point_transform(image, pts):
	# obtain a consistent order of the points and unpack them
	# individually
	rect = order_points(pts)
	(tl, tr, br, bl) = rect

	# compute the width of the new image, which will be the
	# maximum distance between bottom-right and bottom-left
	# x-coordiates or the top-right and top-left x-coordinates
	widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
	widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
	maxWidth = max(int(widthA), int(widthB))

	# compute the height of the new image, which will be the
	# maximum distance between the top-right and bottom-right
	# y-coordinates or the top-left and bottom-left y-coordinates
	heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
	heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
	maxHeight = max(int(heightA), int(heightB))

	# now that we have the dimensions of the new image, construct
	# the set of destination points to obtain a "birds eye view",
	# (i.e. top-down view) of the image, again specifying points
	# in the top-left, top-right, bottom-right, and bottom-left
	# order
	dst = np.array([
		[0, 0],
		[maxWidth - 1, 0],
		[maxWidth - 1, maxHeight - 1],
		[0, maxHeight - 1]], dtype = "float32")

	# compute the perspective transform matrix and then apply it
	M = cv2.getPerspectiveTransform(rect, dst)
	warped = cv2.warpPerspective(image, M, (maxWidth, maxHeight))

	# return the warped image
	return warped


def getROIparams(configFile = "../CharIoT/outputs/config.txt"):
    if(not os.path.isfile(configFile)):
        print("Configuration file not found")
        return

    #Assumes config params: x,y,w,h are put on 4 newline separated lines
    #In a file with no other contents
    intArr =  list(map(int,open(configFile,"r").read().split()))
    tupArr = []
    for i in range(4):
        tupArr.append((intArr[i*2],intArr[i*2+1]))
    return tupArr


def getMorfParams(configFile = "../CharIoT/outputs/config.txt"):
    if(not os.path.isfile(configFile)):
        print("Configuration file not found! Looked for:" + configFile)
        return

    #Assumes config params: x,y,w,h are put on 4 newline separated lines
    #In a file with no other contents
    intArr =  list(map(int,open(configFile,"r").read().split()))
    tupArr = []
    for i in range(4):
        tupArr.append((intArr[i*2],intArr[i*2+1]))
    return tupArr #Should contain 4 tuples corresponding to the 4 points 

print("Performing image transform ---\n")
params = np.array(getMorfParams(sys.argv[1]), dtype = "float32")

if( len(sys.argv) >2 ): #Check if infile specified
	inFile = sys.argv[2]
else:
	inFile = "latest.jpg"
print("Reading from " + inFile + "---\n")

if( len(sys.argv) >3 ): #Check if outfile specified
	endFile = sys.argv[3]
else:
	endFile = "warped.jpg"
print("Saving to " + endFile + "---\n")
print("Using the given parameters for points:" + str(params) + "---\n")

testImg=  cv2.imread(inFile)
endImg = four_point_transform(testImg,params)
#cv2.imshow("Original",testImg)
#cv2.imshow("Warped",endImg)i

print("Attempting to write to: outputs/"+endFile+ " ---\n")
result = cv2.imwrite("outputs/"+endFile, endImg)
print("Warped image written to disk ? "+ str(result))
