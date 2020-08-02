import cv2
import numpy as np
 
frameWidth = 640
frameHeight = 480
cap = cv2.VideoCapture(1)
cap.set(3, frameWidth)
cap.set(4, frameHeight)
 
def empty(a):
    pass
 
cv2.namedWindow("HSV")              # Create a new window
cv2.resizeWindow("HSV", 640, 240)   # Resize window

# Create trackbars
cv2.createTrackbar("HUE Min", "HSV", 0, 179, empty)
cv2.createTrackbar("HUE Max", "HSV", 179, 179, empty)
cv2.createTrackbar("SAT Min", "HSV", 0, 255, empty)
cv2.createTrackbar("SAT Max", "HSV", 255, 255, empty)
cv2.createTrackbar("VALUE Min", "HSV", 0, 255, empty)
cv2.createTrackbar("VALUE Max", "HSV", 255, 255, empty)
 
 
while True:
    success, img = cap.read()
    imgHsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)   # Convert image to HSV (Hue, Saturation, Value)
 
    h_min = cv2.getTrackbarPos("HUE Min", "HSV")
    h_max = cv2.getTrackbarPos("HUE Max", "HSV")
    s_min = cv2.getTrackbarPos("SAT Min", "HSV")
    s_max = cv2.getTrackbarPos("SAT Max", "HSV")
    v_min = cv2.getTrackbarPos("VALUE Min", "HSV")
    v_max = cv2.getTrackbarPos("VALUE Max", "HSV")
    print(h_min)
 
    lower = np.array([h_min, s_min, v_min])     # Lower limit
    upper = np.array([h_max, s_max, v_max])     # Upper limit
    mask = cv2.inRange(imgHsv, lower, upper)    # Filter these colours
    result = cv2.bitwise_and(img, img, mask = mask)     # Where pixels are present in both images, show pixels
 
    mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)   # Convert image to RGB
    hStack = np.hstack([img, mask, result])         # Stack images
    cv2.imshow('Horizontal Stacking', hStack)       # Show stack

    if cv2.waitKey(1) and 0xFF == ord('q'):         # Exit app
        break
 
cap.release()
cv2.destroyAllWindows()