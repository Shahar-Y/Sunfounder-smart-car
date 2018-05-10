import cv2
import numpy as np
import math
import time
import local
from threading import Thread
# Open Camera

capture = cv2.VideoCapture(0)
sleepTime = 0.03
for i in range(0,10):
    time.sleep(sleepTime)
    local.video_dir.move_increase_y()
thread = Thread(target = local.listen)
thread.start()

counter = 0
while capture.isOpened():
    
    # Capture frames from the camera
    ret, frame = capture.read()
    crop_image = frame
    
    # Apply Gaussian blur
    blur = cv2.GaussianBlur(frame, (3,3), 0)
    
    # Change color-space from BGR -> HSV
    hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)
    
    # Create a binary image with where white will be skin colors and rest is black
    mask2 = cv2.inRange(hsv, np.array([165,0,0]), np.array([180,255,255]))
    # 36 70
    # 160 180 pink
    
    # Kernel for morphological transformation    
    kernel = np.ones((5,5))
    
    # Apply morphological transformations to filter out the background noise
    dilation = cv2.dilate(mask2, kernel, iterations = 1)
    erosion = cv2.erode(dilation, kernel, iterations = 1)    
       
    # Apply Gaussian Blur and Threshold
    filtered = cv2.GaussianBlur(erosion, (3,3), 0)
    ret,thresh = cv2.threshold(filtered, 127, 255, 0)
    
    # Show threshold image
    cv2.imshow("Thresholded", thresh)

    # Find contours
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE )
    
    
    try:
        # Find contour with maximum area
        contour = max(contours, key = lambda x: cv2.contourArea(x))
        
        # Create bounding rectangle around the contour
        x,y,w,h = cv2.boundingRect(contour)
        cv2.rectangle(crop_image,(x,y),(x+w,y+h),(0,0,255),0)

        #print x,y,w,h, frame.shape[0], frame.shape[1] 
        if counter%4 == 0:
            local.locate_and_center( x,y,w,h, frame.shape[0],frame.shape[1] )
        counter+=1

        local.locate_and_follow( x,y,w,h, frame.shape[0],frame.shape[1] )

        # Find convex hull
        hull = cv2.convexHull(contour)
        
        # Draw contour
        drawing = np.zeros(crop_image.shape,np.uint8)
        cv2.drawContours(drawing,[contour],-1,(0,255,0),0)
        cv2.drawContours(drawing,[hull],-1,(0,0,255),0)
        
    except:
        pass

    
    # Show required images
    try:
        all_image = np.hstack((drawing, crop_image))
        cv2.imshow('Contours', all_image)
    except:
        pass
      
    # Close the camera if 'q' is pressed
    if cv2.waitKey(1) == ord('q'):
        break

capture.release()
cv2.destroyAllWindows()
