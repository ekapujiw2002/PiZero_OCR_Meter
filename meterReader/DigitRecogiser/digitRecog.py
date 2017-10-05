#####################
# Main digit recognition algorihm
# Gets an image from different sources and tries to detect the digits present
######################

import cv2
import os
import numpy as np
import sys
import os.path
import argparse

#Attempted classifers
from frameSource import ImageSource

from mnistSVC  import  MNISTclassifSVC
from mnistKnn import MNISTclassif
from predict_2 import NNdetect

import time

#Used for colouring terminal output
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
import transformPerspective as transf

#Return a list of labels taken from the given file
#Expects a list of integers
def getLabelList(labelFile = "labels.txt"):
    if(not os.path.isfile(labelFile)):
        print("Label file not found")
        return

    return list(open(labelFile,"r").read().split("\n"))


def getImageList(dirPrefix = "../tutorials/ppplyn-master/images/dataset/1/"): 
    #Get the list of images from a directory
    imgList = os.listdir(dirPrefix)
    i=0                         #Looks at the last 4 characters of the filename (what is an EXIF type)
    while (i<len(imgList)):     #Check file ending, currently only accept png and jpg
        if len(imgList[i])<4 or ( imgList[i][len(imgList[i])-4:] != ".png" and imgList[i][len(imgList[i])-4:] != ".jpg"):
            imgList.remove(imgList[i])
        else:
            i+=1

    #Add the path as prefix
    return [ dirPrefix + elem for elem in imgList]

def getROIparams(configFile = "../CharIoT/outputs/config.txt"):
    if(not os.path.isfile(configFile)):
        print("Configuration file not found")
        return

    #Assumes config params: x,y,w,h are put on 4 newline separated lines
    #In a file with no other contents
    return list(map(int,open(configFile,"r").read().split()))


class DigitDetector:
    cannyLow = -1
    cannyHigh = -1
    singleDigit =False
    flipImage =False
    labelFile = "labels.txt"



    def __init__(self):
        self.camera = ImageSource()
        self.mnistKnn  = MNISTclassif()
        self.mnistSVC =  MNISTclassifSVC()
        self.mnistANN = NNdetect()


    def processArgs(self):

        #Setup argument parser
        parser = argparse.ArgumentParser()
        group = parser.add_mutually_exclusive_group()
        group.add_argument("-pi","--picam",help="Use the camera on the RPi Zero", action='store_true')
        group.add_argument("-d","--directory",help = "Look for images in this directory")
        group.add_argument("-i","--image",help = "Use this image as input")
        group.add_argument("-cam","--webcam",help="Use the webcam for capturing pictures", action= "store_true")
        group.add_argument("-sd","--singleDigit",help="Do not partition the image, use for classfiying a single digit")
        cannyGroup = parser.add_argument_group()
        cannyGroup.add_argument("-cL","--cannyLow",type=int,help = "low threshold for canny edge detection")
        cannyGroup.add_argument("-cH","--cannyHigh",type=int,help = "high threshold for canny edge detection")

        parser.add_argument("--flip",help="Use if image if upside down",action = "store_true")
        parser.add_argument("--label",help="The file in which the list of labels for the input data can be found")
        args = parser.parse_args()

        imgIndex=0
        if(args.cannyLow):
            self.cannyLow = args.cannyLow;
            self.cannyHigh = args.cannyHigh;

        if(args.flip): #Avoid problems with NoneType
            self.flipImage = True
        
        if(args.label):
            self.labelFile  = args.label

        #Check for presence
        if( args.directory):
            print("Was given the following directory: " + bcolors.OKGREEN + args.directory + bcolors.ENDC)
            imgList = getImageList(args.directory)
            return imgList
        elif( args.image ):
            print("Was given the following image file: "+ args.image)
            img = cv2.imread(args.image)
        elif( args.picam):
            print("Using the pi camera")
            img = self.camera.picamLoop()
        elif( args.webcam):
            print("Using webcam capture")
            img = self.camera.webcamCapture()
            img = cv2.flip( img, 1 )        #Flip image
        elif(args.singleDigit):
            self.singleDigit = True
            print("Processing whole image is single digit "+ args.singleDigit)
            img= cv2.imread(args.singleDigit)
        else:
            img= cv2.imread(imgList[imgIndex % len(imgList)])
            print( "INVALID IMAGE ADDRESS GIVEN")
            print( "Now showing from image list: "+ imgList[imgIndex % len(imgList)])
        return img


    def processImage(self,imgName,digits = 6,configFile = "config.txt" ,configDigitFolder= "digitConfigs"):
        #Check if image exists
        #Load image if it hasn't been passsed to the method as a string
        if(isinstance(imgName,str)):
            imgSrc =  cv2.imread(imgName)
        else:
            imgSrc = imgName.copy()

        if(self.singleDigit):
            return self.detectDigit(imgSrc)

        #Load first config file
        #Transform based on file
        warped = transf.configTransform(imgSrc,configFile)
        cv2.imshow("Warped Image",warped)

        print("Writing warped image to disk")
        cv2.imwrite("cropped-meters/"+ str(time.time()) + ".png",warped)
        endDigits = [[],[],[]]
        for i in range(digits):
            #Load second config file (for digits)
            digitConfig = configDigitFolder + "/digits_config_"+str(i)+".txt"
            print(bcolors.OKBLUE + "Now on digit partition \t"+ bcolors.ENDC + str(i))
            #Segment and transform based on second config
            imgDigit = transf.configTransform(warped,digitConfig)
            #Detect in individual images digits
            detectedDigit = self.detectDigit(imgDigit)

            cv2.imshow("Partition: "+str(i), imgDigit.copy())
            endDigits[0].append(detectedDigit[0])
            endDigits[1].append(detectedDigit[1])
            endDigits[2].append(detectedDigit[2])
            print()
 
        print(endDigits)
        return endDigits






    def detectDigit(self,imgSource):
        #Attempt to detect digits
        gray = cv2.cvtColor(imgSource,cv2.COLOR_BGR2GRAY) #Convert to gray
        imgSourceCopy = imgSource.copy()

        #Threshold (with an adaptive threshold) and blur the results
        bin = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C,
                 cv2.THRESH_BINARY_INV, 31, 10)
        bin = cv2.medianBlur(bin, 3)

        #Apply morphological ops
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(10,10))
        bin = cv2.morphologyEx(bin,cv2.MORPH_CLOSE,kernel)
        annBin = cv2.bitwise_not(bin)


        #Ann prediction
        cv2.imwrite("target.png",annBin)

        knnPredicted = self.mnistKnn.classifROI(bin)
        svcPredicted = int(self.mnistSVC.classifROI(bin))
        annPredicted = int(self.mnistANN.detectDigit("target.png"))

        print(bcolors.OKBLUE + "MNIST trained kNN "+ bcolors.ENDC + "prediction of current image :\t"  +  self.mnistKnn.classifROI(bin))
        print(bcolors.OKBLUE + "MNIST trained SVM "+ bcolors.ENDC + "prediction of current image :\t"  +  self.mnistSVC.classifROI(bin))
        print(bcolors.OKBLUE + "MNIST trained ANN "+ bcolors.ENDC + "prediction of current image :\t"  +  str(annPredicted))
        cv2.imshow("Bin to be sent to MNIST",bin)

        return [knnPredicted, svcPredicted, annPredicted]


###########################
# Commands to be executed #
###########################
digitDetect = DigitDetector()

imgIndex=0
imgSelection = digitDetect.processArgs()
labels = getLabelList(digitDetect.labelFile)

#Initialise array keeping track of digits/line classification accuracy
digits = 4

if(labels): #Check that some labels have been loaded
    totalRight = [0 for i in range(3)]
    totalDigits= [0 for i in range(3)]


while True: 
    print(bcolors.HEADER +"--------------------------------------------------" + bcolors.ENDC)
    print("-----------Now on image "+ bcolors.OKGREEN + str(imgIndex) + bcolors.ENDC + " of directory----------") 
    
    #If given a directory, the image selection will be a list of images
    #If given a single image, it will be a list with 1 element
    img= cv2.imread(imgSelection[imgIndex % len(imgSelection)])

    #See if the image needs to be flipped before processing 
    #(i.e. fix it being upside down)
    if(digitDetect.flipImage):
        img = cv2.flip(img,-1)
    #cv2.imshow("Original, read from file",img)

    #Do the digit detection using the class, print the result

    #singleDigit = str(digitDetect.detectDigit(img))
    readLine = digitDetect.processImage(img,digits)

    try:
        #Compare to label, count rightly detected digits
        if(labels):
            for i in range(3):
                for j in [0,1,2,3]:
                    print("Comparing \t" + str(readLine[i][j]) + " to\t" + str(labels[imgIndex][j]))
                    if( int(readLine[i][j]) == int(labels[imgIndex][j])):
                        totalRight[i] +=1
        #Display returned number
                print(bcolors.OKGREEN + "Number detected as returned \t\t" + bcolors.ENDC + str(readLine[i][:4]))
    except:
        #Result of detection does not have 4 digits, likely an error in vision
        print(bcolors.WARNING + "Number has incorrect format as returned \t" + bcolors.ENDC + str(readLine[i]))

    if(labels):
        for i in range(3):
            totalDigits[i] += digits
        print(bcolors.WARNING + "Compare to manually set label \t\t" + bcolors.ENDC + labels[imgIndex % (len(labels)-1)]) 
        print(bcolors.HEADER +"--------------------------------------------------\n\n" + bcolors.ENDC)

    imgIndex+=1         #Update image index
    print(bcolors.HEADER +"--------------------------------------------------\n\n" + bcolors.ENDC)

    #If we're done with the files in the directory
    #Display the overall accuracy
    if( isinstance(imgSelection,list) and imgIndex == len(imgSelection) and labels):
        print(bcolors.HEADER +"--------------------------------------------------" + bcolors.ENDC)

        for i in range(3):
            print("Of a total of "+ str(totalDigits[i]) + " digits, "+ str(totalRight[i]) + " have been correctly identified")
            print("Giving this a total accuracy of " + bcolors.OKGREEN+ str(float(totalRight[i]*100/totalDigits[i]))+ "%" + bcolors.ENDC)
        print(bcolors.HEADER +"--------------------------------------------------" + bcolors.ENDC)
        break

    cv2.waitKey(1000)   #Wait for a bit
    print("\033c")      #Clean screen (console output)
