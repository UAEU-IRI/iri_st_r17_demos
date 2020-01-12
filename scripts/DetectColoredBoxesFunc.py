
# import the necessary packages
from collections import deque
import numpy as np
#import argparse
import imutils
import cv2

 
# define the lower and upper boundaries of the colors in the HSV color space
lower = {'red':(0, 170, 90), 'blue':( 30,80,50), 'yellow':(10,80,150)} #assign new item 'green':(66, 122, 129),, 'red':(166, 84,141) 'orange':(0, 50, 80) lower['blue'] = (93, 10, 0)
upper = {'red':(175,255,255), 'blue':(117,255,255), 'yellow':( 50,200,255)} #'green':(86,255,255),'orange':(20,255,255),'red':(186,255,255),

# define standard colors for circle around the object
colors = {'red':(0,0,255),  'blue':(255,0,0), 'yellow':(0, 255, 255)} #'green':(0,255,0),, 'orange':(0,140,255)

global RedCubePlace,BlueCubePlace,YellowCubePlace
YellowCubePlace = None
RedCubePlace = None
BlueCubePlace = None

# Returns (RedCubePlace,BlueCubePlace,YellowCubePlace)
def DetectColoredBoxLocation(frame):
    global RedCubePlace,BlueCubePlace,YellowCubePlace

 
    # resize the frame, blur it, and convert it to the HSV
    # color space
    frame = imutils.resize(frame, width=600)

    blurred = cv2.GaussianBlur(frame, (11, 11), 0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
    #for each color in dictionary check object in frame
    for key, value in upper.items():
        # construct a mask for the color from dictionary`1, then perform
        # a series of dilations and erosions to remove any small
        # blobs left in the mask
        kernel = np.ones((9,9),np.uint8)
        mask = cv2.inRange(hsv, lower[key], upper[key])
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
                
        # find contours in the mask and initialize the current
        # (x, y) center of the ball
        cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE)[-2]
        center = None
        
        # only proceed if at least one contour was found
        if len(cnts) > 0:
            # find the largest contour in the mask, then use
            # it to compute the minimum enclosing circle and
            # centroid
            c = max(cnts, key=cv2.contourArea)
            ((x, y), radius) = cv2.minEnclosingCircle(c)
            M = cv2.moments(c)
            center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

            rect = cv2.minAreaRect(c)
            #print(rect)
            box = cv2.boxPoints(rect)
            box = np.int0(box)
      
            #Reset Slots each Iteration:
            #S1SLOT = None
            #S2SLOT = None
            #S3SLOT = None
            #S4SLOT = None
            #YellowCubePlace = None
            #RedCubePlace = None
            #BlueCubePlace = None
        
            # only proceed if the radius meets a minimum size. Correct this value for your obect's size
            if radius > 10.9:
                # draw the circle and centroid on the frame,
                # then update the list of tracked points
                cv2.drawContours(frame,[box],0,colors[key],2)
                #cv2.circle(frame, (int(x), int(y)), int(radius), colors[key], 2)
                cv2.putText(frame,key + " cube", (int(x-radius),int(y-radius)), cv2.FONT_HERSHEY_SIMPLEX, 0.6,colors[key],2)
                
                if (center[0]>=194 and center[0]<=235 and center[1]>=65 and center[1]<=93):	#S4 Slot Position in Pixels
                    #print(key+" cube is in slot S4")
                    #S4SLOT = key
                    if (key == 'yellow'):
                        YellowCubePlace = 'S4'
                    elif (key == 'red'):
                        RedCubePlace = 'S4'
                    elif (key == 'blue'):
                        BlueCubePlace = 'S4'

                if (center[0]>=330 and center[0]<=376 and center[1]>=198 and center[1]<=226):	#S3 Slot Position in Pixels
                    #print(key+" cube is in slot S3")
                    #S3SLOT = key
                    if (key == 'yellow'):
                        YellowCubePlace = 'S3'
                    elif (key == 'red'):
                        RedCubePlace = 'S3'
                    elif (key == 'blue'):
                        BlueCubePlace = 'S3'
                
                if (center[0]>=526 and center[0]<=599 and center[1]>=253 and center[1]<=297):	#S2 Slot Position in Pixels
                    #print(key+" cube is in slot S2")
                    #S2SLOT = key
                    if (key == 'yellow'):
                        YellowCubePlace = 'S2'
                    elif (key == 'red'):
                        RedCubePlace = 'S2'
                    elif (key == 'blue'):
                        BlueCubePlace = 'S2'

                if (center[0]>=73 and center[0]<=107 and center[1]>=338 and center[1]<=373):	#S1 Slot Position in Pixels
                    #print(key+" cube is in slot S1")
                    #S1SLOT = key
                    if (key == 'yellow'):
                        YellowCubePlace = 'S1'
                    elif (key == 'red'):
                        RedCubePlace = 'S1'
                    elif (key == 'blue'):
                        BlueCubePlace = 'S1'

                #print ("Center of " + key + " cube:" ,center)
                #print ("Cubes Places: RED	BLUE	YELLOW")
                #print ('		',RedCubePlace,'	',BlueCubePlace,'	',YellowCubePlace)

    # show the frame to our screen
    frame = imutils.resize(frame, width=1400)
    cv2.flip(frame, flipCode=-1)
    cv2.imshow("Frame", frame)
    cv2.waitKey(1)
    return [RedCubePlace,BlueCubePlace,YellowCubePlace]


