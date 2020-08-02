import cv2
import numpy as np

frameWidth = 640
frameHeight = 480

cap = cv2.VideoCapture(1)   # Get webcam, 0 = default id
cap.set(3, frameWidth)      # Set width
cap.set(4, frameHeight)     # Set height

# Highlighter colors
myColors = [[146, 157, 83, 179, 211, 255],      # Pink
            [22, 39, 156, 65, 109, 255],        # Yellow
            [0, 112, 139, 16, 229, 255],        # Orange
            [65, 69, 78, 92, 213, 255]]         # Green

# BGR
myColorValues = [[102, 0, 204],
                 [102, 255, 178], 
                 [0, 102, 204],
                 [51, 102, 0]]
            
myPoints = []   # x, y, colorID

def findColor(img, myColors, myColorValues):
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)       # Convert image to HSV (Hue, Saturation, Value)
    count = 0
    newPoints = []

    for color in myColors:
        lower = np.array(color[0:3])                # Lower limit
        upper = np.array(color[3:6])                # Upper limit
        mask = cv2.inRange(imgHSV, lower, upper)    # Filter these colours

        x, y = getContours(mask)
        cv2.circle(imgResult, (x, y), 10, myColorValues[count], cv2.FILLED)      # Draw blue circle at centre top position of bounding box

        if x != 0 and y != 0:
            newPoints.append([x, y, count])

        count += 1
        #cv2.imshow(str(color[0]), mask)
    return newPoints

def getContours(img):
    contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)   # Get all contours
    x, y, w, h = 0, 0, 0, 0

    for cnt in contours:
        area = cv2.contourArea(cnt)     # Calculate area of contour

        if area > 500:
            #cv2.drawContours(imgResult, cnt, -1, (255, 0, 0), 3)   # Draw blue contour around shape
            peri = cv2.arcLength(cnt, True)                        # Calculate perimeter of contour

            approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)      # Calculate corner points of contour
            x, y, w, h = cv2.boundingRect(approx)                  # Calculate x, y, w, h bounds of contour
    return x + (w // 2), y      # Return centre top position of bounding box (x = centre, y = top)

def drawOnCanvas(myPoints, myColorValues):
    for point in myPoints:
        cv2.circle(imgResult, (point[0], point[1]), 10, myColorValues[point[2]], cv2.FILLED)

while True:
    success, img = cap.read()   # While another frame exists, read it
    imgResult = img.copy()
    newPoints = findColor(img, myColors, myColorValues)

    if len(newPoints) != 0:
        for newP in newPoints:
            myPoints.append(newP)

    # Draw
    if len(myPoints) != 0:
        drawOnCanvas(myPoints, myColorValues)

    cv2.imshow("Video", imgResult)    # Show frame

    if cv2.waitKey(1) & 0xFF == ord('q'):   # If 'q' is pressed, end video
        break