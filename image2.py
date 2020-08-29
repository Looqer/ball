from collections import deque
import cv2
import numpy as np
import imutils
import argparse

ap = argparse.ArgumentParser()
ap.add_argument("-b", "--buffer", type=int, default=64, help="max buffer size")
args=vars(ap.parse_args())
pts = deque(maxlen=args["buffer"])

cam = cv2.VideoCapture(0)

while True:
    
    

    l_orange = np.array([40,40,40])
    u_orange = np.array([70,255,255])
    
    b, img = cam.read()
    

    
    
    if b:
        rotated = cv2.rotate(img, cv2.ROTATE_180)
        final = cv2.convertScaleAbs(rotated, alpha =3, beta  = 0)
        hsv = cv2.cvtColor(rotated, cv2.COLOR_BGR2HSV)
        masked = cv2.inRange(hsv, l_orange, u_orange)
        scary = cv2.bitwise_and(rotated, rotated, mask = masked)
        
        cnts = cv2.findContours(masked.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
        cnts = imutils.grab_contours(cnts)
        center = None
        
        
        if len(cnts) > 0:
        
            c = max(cnts, key=cv2.contourArea)
            ((x, y), radius) = cv2.minEnclosingCircle(c)
            M = cv2.moments(c)
            if M["m00"] > 0:
                center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
        
            if radius > 10:
           
                cv2.circle(rotated, (int(x), int(y)), int(radius),
                    (0, 255, 255), 2)
                cv2.circle(rotated, center, 5, (0, 0, 255), -1)
                xr = round(x,1)
                yr = round(y,1)
                cv2.putText(rotated, ("position x %s " % xr+"position y %s" % yr), (10,20), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,0), 2)
    
        pts.appendleft(center)
        
        cv2.imshow("Window 1",rotated)
        #cv2.imshow("Window 2",final)
        #cv2.imshow("Window 3",masked)
        #cv2.imshow("Window 4",scary)

        
        cv2.waitKey(1)
        
    else:
        print("The camera is not working!")
        break
    
    key = cv2.waitKey(1)&0xFF
    if key==ord('q'):
        break
    
cv2.destroyAllWindows()
cam.release()
