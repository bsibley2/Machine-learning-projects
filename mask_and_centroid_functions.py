import numpy as np
import cv2 


def make_mask(frame):
    lower_blue = np.array([110,50,50]) # lower hsv bound for blue
    upper_blue = np.array([130,255,255]) # upper hsv bound to blue
    
    element = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    
    hsv=cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    mask=cv2.inRange(hsv,lower_blue,upper_blue)
    
    mask2 = cv2.dilate(mask, element)
    mask2 = cv2.erode(mask2, element)
    return mask2

def get_centroid(mask):
    retval, labels, stats, centroids = cv2.connectedComponentsWithStats(mask)
    max_i = np.argmax(stats[1:, 4]) + 1
    max_area = stats[max_i, 4]
    return centroids[max_i]