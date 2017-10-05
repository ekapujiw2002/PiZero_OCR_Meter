#Segment an image based on 4 user selected points
# Click on image to select 4 point
# Press Enter to accept selection
# Press "R" to select again

import cv2
import numpy as np
import sys
import transform as transf
points =0
pointArr = []

def scaleX(x):
    return int( (x*imgWidth) / dispWidth)

def scaleY(y):
    return int( (y*imgHeight / dispHeight))

# mouse callback function
def draw_circle(event,x,y,flags,param):
    global points
    global pointArr
    if(event == 1 and points <4 ):
        print("A CLICK HAPPENED at "+ str(x) + " - " + str(y))
        print("Event string is: " + str(event))
        pointArr.append((x,y))
        points+=1
    elif event == cv2.EVENT_LBUTTONDBLCLK:
        cv2.circle(img,(x,y),100,(255,0,0),-1)
    #else:
        #print("Event string is: " + str(event))

# Create a black image, a window and bind the function to window
img = cv2.imread(sys.argv[1])

parts =1

if(len(sys.argv) > 2 ):
    # take the second argument as the number of partitions to determine
    parts = int(sys.argv[2])


imgWidth = img.shape[1]
imgHeight = img.shape[0]
print(str(imgWidth) + " Is image width")
print(str(imgHeight) + " Is iamge heigth")
dispWidth = 1067
dispHeight = 800

imgDisp = cv2.resize(img,(dispWidth,dispHeight),interpolation= cv2.INTER_AREA)


cv2.namedWindow('image', flags= cv2.WINDOW_FREERATIO)
cv2.setMouseCallback('image',draw_circle)
cp =0


while(1):
    cv2.imshow('image',imgDisp)
    #Write points to file
    if(points == 4):
        print("4 points selected for partition " + str(cp) + "  save by pressing space")
        pointArr = [ (scaleX(point[0]),scaleY(point[1])) for point in pointArr]
        print("----------")
        for i in range(len(pointArr)):
            print(str(pointArr[i][0]) + " " + str(pointArr[i][1]))
        print("----------")


        ans = cv2.waitKey()
        if(ans == 32): #Space pressed
            print("Point written to file")
            fileName ='config_' + str(cp)+'.txt'
            resultImageName = "outputs/warped_"+ str(cp)+ ".png"
            f = open(fileName, 'w')
            for i in range(len(pointArr)):
                f.write(str(pointArr[i][0]) + " " + str(pointArr[i][1])+ "\n")
            f.close()

            warped = transf.configTransform(img,fileName)
            cv2.imshow("Result of choice", warped)
            cv2.imwrite(resultImageName,warped)

            print("Press space again to confirm and exit")
            ans2 = cv2.waitKey()
            if(ans2 == ans):
                print("Successfully selected a ROI")
                cp+=1

                #Reset points so new ones can be selected
                points =0
                pointArr.clear()
                if(cp == parts):
                    print("All partitions selected")
                    break
            else:   #if(ans2== 82 or ans2==114): #Upper/lowercase R
                print("Point not saved, please reselect")
                points =0
                pointArr.clear()
        else:
            print("Point not saved, please reselect")
            points =0
            pointArr.clear()

    if cv2.waitKey(20) & 0xFF == 27:
        print("Exiting segmentation program")
        break
cv2.destroyAllWindows()
