# import the necessary packages
from __future__ import print_function
from sklearn.cross_validation import train_test_split
from sklearn.metrics import classification_report
from sklearn.svm import LinearSVC
from sklearn.externals import joblib


from sklearn import datasets
from skimage import exposure
import numpy as np
import imutils
import cv2
import sys
# load the MNIST digits dataset
from mnist import MNIST

# Classify an incoming image
# Using a SVC (suppport vector machine based classifier)
# Trained on the MNIST dataset
class MNISTclassifSVC:
    def __init__(self):
        try:
            #Check if a trained model exists
            self.model = joblib.load("digits_model_linearSVC.pkl")
        except:
            #Otherwise train on the MNIST dataset
            #mnist = datasets.load_digits()

            #Replacement MNIST data
            mndata = MNIST('./data')
            MNISTtrainImages, MNISTtrainLabels = mndata.load_training()
            MNISTtestImages,MNISTtestLabels =  mndata.load_testing()

            MNISTtrainImages = np.array(MNISTtrainImages)
            MNISTtestImages = np.array(MNISTtestImages)

            MNISTtrainLabels = np.array(MNISTtrainLabels)
            MNISTtestLabels = np.array(MNISTtestLabels)
 
            #Debug code for MNIST data
            #print(MNISTtrainImages.shape)
            #print ("Training data of shape"+ str(trainData.shape))
            #print (trainData)
            #print("\n\nTraining labels" + str(trainLabels.shape))
            #print (trainLabels)


            # now, let's take 10% of the training data and use that for validation
            #(trainData, valData, trainLabels, valLabels) = train_test_split(trainData, trainLabels, test_size=0.1, random_state=84)

            (trainData, valData, trainLabels, valLabels) = train_test_split(MNISTtrainImages, MNISTtrainLabels, test_size=0.1, random_state=84)
            #print("Train data dimensions (MNIST only):")
            #print(trainData.shape)
            #print("\n\n\n\n")

            ''' Insert new data (examples from segemnted digits)
            for i in range(10):
                #newData = self.imageToSample("/Users/stbogdan/OneDrive/Internship-CharIoT/MeterPictures/digital-Digits/real-"+ str(i) +".jpg",i)

                #TODO Move this outside if memory requirement too high
                newDataArray = np.array(newData[0])
                #print("Compare these dimensions:")
                #print(trainData.shape)
                #print(newDataArray.shape)

                #Add new data to set (TODO Might be worth doing at the end)
                if( isinstance(trainData,int) and  trainData == -1):
                    trainData = np.array([newDataArray])
                    trainLabels = np.array([int(newData[1])])
                else:
                    trainData = np.concatenate([trainData,[newDataArray]]) #Extra brackets as new data is [<newSample>], where newSample is itself an array
                    trainLabels = np.concatenate([trainLabels,[int(newData[1])]])
                print("Added new data to training with label "+ str(newData[1]) + " matching "+ str(i))            
            print("Train data dimensions after adding some image data:")
            print(trainData.shape)
            print("\n\n\n\n")
            '''

            #Show the sizes of each data split
            print("training data points: {}".format(len(trainLabels)))
            print("validation data points: {}".format(len(valLabels)))
            print("testing data points: {}".format(len(testLabels)))

            #Load the model by initialising a new 
            self.model = LinearSVC()

            print("Fitting data")
            self.model.fit(trainData, trainLabels)

            print("Predicting test images")
            predictions = self.model.predict(MNISTtestImages)
 
            # show a final classification report demonstrating the accuracy of the classifier
            # for each of the digits
            print("EVALUATION ON TESTING DATA")
            print(classification_report(MNISTtestLabels, predictions))

            # save model for later use
            print("Saving trained model")
            joblib.dump(self.model,"digits_linearSVC.pkl",compress=3)

    def classifROI(self,img):
        # grab the image and classify it
        imageSource = img.copy()
        cv2.imshow("Original",imageSource)

        #These operations done in process image
        #image= cv2.bitwise_not(image)
        #_, image = cv2.threshold(image,127,255,cv2.THRESH_BINARY)
        #gray  =cv2.cvtColor(imageSource,cv2.COLOR_BGR2GRAY)
        #image = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C,
                # cv2.THRESH_BINARY_INV, 31, 10)
        '''
        #Check all the resizing modes to choose the best for digit shape retention
        imgLinear   = cv2.resize(image,(8,8), interpolation = cv2.INTER_LINEAR)
        imgNearest  = cv2.resize(image,(8,8), interpolation = cv2.INTER_NEAREST)
        imgArea     = cv2.resize(image,(8,8), interpolation = cv2.INTER_AREA)
        imgCubic    = cv2.resize(image,(8,8), interpolation = cv2.INTER_CUBIC)
        imgLanc     = cv2.resize(image,(8,8), interpolation = cv2.INTER_LANCZOS4)

        resArr = [imgLinear,imgNearest,imgArea,imgCubic,imgLanc]
        resPred =[]
        for i in range(0,len(resArr)):
            classifInput = resArr[i].reshape((1,64))
            classifPred   =self.model.predict(classifInput)[0]
            resPred.append(classifPred)
        print("PREDICTIONS ARE IN:" + str(resPred))

        imgLinear  = imutils.resize( imgLinear, width=32,inter=cv2.INTER_LINEAR)
        imgNearest = imutils.resize( imgNearest, width=32,inter=cv2.INTER_LINEAR)
        imgArea    = imutils.resize( imgArea, width=32,inter=cv2.INTER_LINEAR)
        imgCubic   = imutils.resize(imgCubic, width=32,inter=cv2.INTER_LINEAR)
        imgLanc    = imutils.resize( imgLanc, width=32,inter=cv2.INTER_LINEAR)

        cv2.imshow("Resize options",np.hstack([imgLinear,imgNearest,imgArea,imgCubic,imgLanc]))
        '''
        image = img.copy()
        image = cv2.resize(image,(28,28), interpolation = cv2.INTER_AREA)   #MNIST samples are 28x28 pictures
        image = image.reshape((1,784))                                      #Flatten to a one dimensional vector

        #print(image)
        #print(testData[i])
        prediction = self.model.predict(image)[0]


        # convert the image from a 64-dim array to an 8 x 8 image compatible with OpenCV,
        # then resize it to 32 x 32 pixels so we can see it better
        image = image.reshape((28, 28)).astype("uint8")
        image = exposure.rescale_intensity(image, out_range=(0, 255))
        image = imutils.resize(image, width=32, inter=cv2.INTER_LINEAR)

        # show the prediction
        #print("I think that digit is: {}".format(prediction))
        cv2.imshow("MNIST input", image)
        return str(prediction)

    def imageToSample(self, imgFileName,label):
        #Read img
        imgSource =cv2.imread(imgFileName)
        #Covert to gray
        gray = cv2.cvtColor(imgSource,cv2.COLOR_BGR2GRAY) #Convert to gray

        #Threshold
        imgThresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C,
                 cv2.THRESH_BINARY_INV, 31, 10)
        imgThresh = cv2.medianBlur(imgThresh, 3)

        #Apply morphological ops
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(10,10))
        imgThresh = cv2.morphologyEx(imgThresh,cv2.MORPH_CLOSE,kernel)
        
        #Resize to 28x28
        imgSmall = cv2.resize(imgThresh,(28,28), interpolation = cv2.INTER_AREA)
        
        cv2.imshow(str(label), imgSmall)
        #cv2.waitKey()
        #Flatten
        imgsmol = np.ravel(imgSmall)
        #Return with label attached
        return (imgsmol,label)



