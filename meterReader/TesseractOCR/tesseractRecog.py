#####################
# Main digit recognition algorihm
# Gets an image from different sources and tries to detect the digits present
# Now using tesseract
# https://github.com/tesseract-ocr/tesseract
######################

import cv2
import os
import numpy as np
import sys
import os.path
import argparse


from frameSource import ImageSource
import transformPerspective as transf


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

#Returns a list of the .png and .jpg images in a given directory
#As list of file paths
#Note: uses suffix matching to get image files
def getImageList(dirPrefix ):

    imgList = os.listdir(dirPrefix)     #List all files
    i=0                                 #Looks at the last 4 characters of the filename (what is an EXIF type)
    while (i<len(imgList)):             #Check file ending, currently only accept png and jpg
        if len(imgList[i])<4 or ( imgList[i][len(imgList[i])-4:] != ".png" and imgList[i][len(imgList[i])-4:] != ".jpg"):
            imgList.remove(imgList[i])
        else:
            i+=1

    #Add the path as prefix
    return [ dirPrefix + elem for elem in imgList]

#Return a list of labels taken from the given file
#Expects a list of integers
def getLabelList(labelFile = "labels.txt"):
    if(not os.path.isfile(labelFile)):
        print("Label file not found")
        return

    return list(open(labelFile,"r").read().split("\n"))

#Return a list of numbers from a configuration file 
#Expects 4 lines, each containing space separated x,y coordinates
def getROIparams(configFile): 
    if(not os.path.isfile(configFile)):
        print("Configuration file not found")
        return

    #Assumes config params: x,y,w,h are put on 4 newline separated lines
    #In a file with no other contents
    return list(map(int,open(configFile,"r").read().split()))

#Main class
#Handles command line arguments
#Handles image pre-processing
#Handles recognition
class TesseractDigitDetector:

    #Default parameters
    flipImage =False
    labelFile = "labels.txt"

    #Default adaptive threshold params (can be overriden on run)
    threshC= 10
    blockSize= 85

    def __init__(self):
        self.camera = ImageSource()

    def processArgs(self):

        #Setup argument parser
        parser = argparse.ArgumentParser()

        #Image source config
        group = parser.add_mutually_exclusive_group()
        group.add_argument("-pi","--picam",help="Use the camera on the RPi Zero", action='store_true')
        group.add_argument("-d","--directory",help = "Look for images in this directory")
        group.add_argument("-i","--image",help = "Use this image as input")
        group.add_argument("-cam","--webcam",help="Use the webcam for capturing pictures", action= "store_true")

        parser.add_argument("--flip",help="Use if image if upside down",action = "store_true")
        parser.add_argument("--label",help="The file in which the list of labels for the input data can be found")

        #Thresholding parameters
        threshGroup = parser.add_argument_group()
        threshGroup.add_argument("-bs", "--blockSize",type=int,help = "Block size for adaptive thresholding")
        threshGroup.add_argument("-c","--substractConstant",type=int,help="Constant substracted from calculated mean")
        args = parser.parse_args()

        imgIndex=0

        if(args.flip): #Avoid problems with NoneType
            self.flipImage = True

        if(args.blockSize):
            self.blockSize = int(args.blockSize)
            self.threshC   = int(args.substractConstant)

        if(args.label):
            self.labelFile = args.label

        #Find image source
        if( args.directory):
            print("Was given the following directory: " + bcolors.OKGREEN + args.directory + bcolors.ENDC)
            imgList = getImageList(args.directory)
            return imgList
        elif( args.image ):
            print("Was given the following image file: "+ args.image)
            img = [args.image] 
            #If a dir is given, a list of images is returned
            #Here a list containing one image is returned for consistency
        elif( args.picam):
            print("Using the pi camera")
            img = self.camera.picamLoop()
        elif( args.webcam):
            print("Using webcam capture")
            img = self.camera.webcamCapture()
            img = cv2.flip( img, 1 )        #Flip image
        else:
            img= cv2.imread(imgList[imgIndex % len(imgList)])
            print( "INVALID IMAGE ADDRESS GIVEN")
            print( "Now showing from image list: "+ imgList[imgIndex % len(imgList)])
        return img


    def processImage(self,imgName,lines= 6,configFile = "config.txt" ,configLineFolder= "lineConfigs"):

        #Check if image exists
        #Load image if it hasn't been passsed to the method as a string
        if(isinstance(imgName,str)):
            imgSrc =  cv2.imread(imgName)
        else:
            imgSrc = imgName.copy()

        #Load first config file
        #Transform based on file
        warped = transf.configTransform(imgSrc,configFile)
        cv2.imshow("Warped Image",warped)

        #print("Writing warped image to disk")
        #cv2.imwrite("cropped-meters/"+ str(time.time()) + ".png",warped)
        endLines=[]
        for i in range(lines):
            #Load second config file (for each line)
            digitConfig = configLineFolder + "/line_config_"+str(i)+".txt"
            print(bcolors.OKBLUE + "Now on line \t"+ bcolors.ENDC + str(i))

            #Segment and transform based on second config
            imgLine = transf.configTransform(warped,digitConfig)

            result = self.detectLine(imgLine)
            cv2.imshow("Partition: "+str(i), imgLine.copy())
            print(bcolors.OKBLUE + "Result of line read\t"+ bcolors.ENDC+ str(result))


            #Remove not-digits
            result = ''.join(filter(lambda x: x.isdigit(), result))
            #Add the result to the result array
            endLines.append(result)

        print(endLines)
        return endLines

    def detectLine(self,imgSource):
        #Perform OCR for line

        #Write the image 
        gray = cv2.cvtColor(imgSource,cv2.COLOR_BGR2GRAY) #Convert to gray
        imgSourceCopy = imgSource.copy()

        #Threshold (with an adaptive threshold) and blur the results
        bin = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C,
                 cv2.THRESH_BINARY_INV, self.blockSize, self.threshC)  #Was 31
        bin = cv2.medianBlur(bin, 3)
        bin = cv2.bitwise_not(bin)
        lineImage = "Partition"+".jpg"

        cv2.imshow("Current partition",bin)
        cv2.imwrite(lineImage,bin)
        #Call tesseract on the image 
        #TODO Use the python wrapper instead of the system call
        stream = os.popen("tesseract "+lineImage+" stdout --psm 9 digits")
        result = stream.read().strip()

        return str(result)

###########################
# Commands to be executed #
###########################
digitDetect = TesseractDigitDetector()

imgIndex=0
imgSelection = digitDetect.processArgs()
labels = getLabelList(digitDetect.labelFile)

#Initialise array keeping track of digits/line classification accuracy
lines =1

if(labels): #Check that some labels have been loaded
    totalRight = [0 for i in range(lines)]
    totalDigits= [0 for i in range(lines)]


while True: #Iterate through the images given as arguments
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
    readLines = digitDetect.processImage(img,lines)
    for i in range(lines):
        try:
            #Compare to label, count rightly detected digits
            if(labels):
                for j in [0,1,2,3]:
                    print("Comparing \t" + readLines[i][j] + " to\t" + labels[imgIndex][j])
                    if( readLines[i][j] == labels[imgIndex][j]):
                        totalRight[i] +=1
            #Display returned number
            print(bcolors.OKGREEN + "Number detected as returned \t\t" + bcolors.ENDC + readLines[i][:4])
        except:
            #Result of detection does not have 4 digits, likely an error in vision
            print(bcolors.WARNING + "Number not of format as returned \t" + bcolors.ENDC + readLines[i])

        if(labels):
            totalDigits[i] +=4
            print(bcolors.WARNING + "Compare to manually set label \t\t" + bcolors.ENDC + labels[imgIndex % (len(labels)-1)]) 
        print(bcolors.HEADER +"--------------------------------------------------\n\n" + bcolors.ENDC)

    imgIndex+=1         #Update image index

    #If we're done with the files in the directory
    #Display the overall accuracy
    if( isinstance(imgSelection,list) and imgIndex == len(imgSelection) and labels):
        print(bcolors.HEADER +"--------------------------------------------------" + bcolors.ENDC)
        for i in range(lines):
            print("On line " + bcolors.OKGREEN + str(i) + bcolors.ENDC)
            print("Of a total of "+ str(totalDigits[i]) + " digits, "+ str(totalRight[i]) + " have been correctly identified")
            print("Giving this a total accuracy of " + bcolors.OKGREEN+ str(float(totalRight[i]*100/totalDigits[i]))+ "%" + bcolors.ENDC)
        print(bcolors.HEADER +"--------------------------------------------------" + bcolors.ENDC)
        break


    cv2.waitKey(1000)   #Wait for a bit
    print("\033c")      #Clean screen (console output)
