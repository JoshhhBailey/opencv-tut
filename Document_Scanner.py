import cv2
import numpy as np

imageWidth = 960
imageHeight = 540

warpedWidth = 600
warpedHeight = 800

cap = cv2.VideoCapture(1)   # Get webcam, 0 = default id

def preProcessing(img):
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)     # Convert to grayscale
    imgBlur = cv2.GaussianBlur(imgGray, (5, 5), 1)      # Blur
    imgCanny = cv2.Canny(imgBlur, 200, 200)             # Detect edges

    kernel = np.ones((5, 5))
    imgDilation = cv2.dilate(imgCanny, kernel, iterations = 2)      # Increase contour thickness
    imgThreshold = cv2.erode(imgDilation, kernel, iterations = 1)   # Slightly erode contour thickness

    return imgThreshold

def getContours(img):
    biggest = np.array([])
    maxArea = 0
    contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)   # Get all contours

    for cnt in contours:
        area = cv2.contourArea(cnt)     # Calculate area of contour

        if area > 2500:
            peri = cv2.arcLength(cnt, True)                         # Calculate perimeter of contour
            approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)   # Calculate corner points of contour

            # Find 4 sided contour with the biggest area
            if area > maxArea and len(approx) == 4:
                biggest = approx
                maxArea = area
    cv2.drawContours(imgContour, biggest, -1, (255, 0, 0), 20)   # Draw blue points around largest contour
    return biggest

# Sort points in order: TopL, TopR, BotL, BotR
def reorder(myPoints):
    
    myPoints = myPoints.reshape((4, 2))             # Change array to 4 x 2, from 4 x 1 x 2
    myPointsNew = np.zeros((4, 1, 2), np.int32)

    add = myPoints.sum(1)                           # Sum X and Y of points
    myPointsNew[0] = myPoints[np.argmin(add)]       # Find and assign smallest number
    myPointsNew[3] = myPoints[np.argmax(add)]       # Find and assign largest number

    difference = np.diff(myPoints, axis = 1)
    myPointsNew[1] = myPoints[np.argmin(difference)]    # Find and assign second largest number
    myPointsNew[2] = myPoints[np.argmax(difference)]    # Find and assign third largest number

    return myPointsNew

def getWarp(img, biggest):
    biggest = reorder(biggest)

    pts1 = np.float32(biggest)                                                          # Matrix of biggest contour points
    pts2 = np.float32([[0, 0], [imageWidth, 0], [0, imageHeight], [imageWidth, imageHeight]])   # TopL, TopR, BotL, BotR
    matrix = cv2.getPerspectiveTransform(pts1, pts2)                                    # Get transformation matrix
    imgOutput = cv2.warpPerspective(img, matrix, (imageWidth, imageHeight))             # Warp image

    imgCropped = imgOutput[20:imgOutput.shape[0] - 20, 20:imgOutput.shape[1] - 20]      # Crop 20 pixels off X and Y
    imgCropped = cv2.resize(imgCropped, (imageHeight, imageWidth))

    return imgCropped

def stackImages(scale, imgArray):
    rows = len(imgArray)
    cols = len(imgArray[0])
    rowsAvailable = isinstance(imgArray[0], list)
    width = imgArray[0][0].shape[1]
    height = imgArray[0][0].shape[0]
    if rowsAvailable:
        for x in range ( 0, rows):
            for y in range(0, cols):
                if imgArray[x][y].shape[:2] == imgArray[0][0].shape [:2]:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (0, 0), None, scale, scale)
                else:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (imgArray[0][0].shape[1], imgArray[0][0].shape[0]), None, scale, scale)
                if len(imgArray[x][y].shape) == 2: imgArray[x][y]= cv2.cvtColor( imgArray[x][y], cv2.COLOR_GRAY2BGR)
        imageBlank = np.zeros((height, width, 3), np.uint8)
        hor = [imageBlank]*rows
        hor_con = [imageBlank]*rows
        for x in range(0, rows):
            hor[x] = np.hstack(imgArray[x])
        ver = np.vstack(hor)
    else:
        for x in range(0, rows):
            if imgArray[x].shape[:2] == imgArray[0].shape[:2]:
                imgArray[x] = cv2.resize(imgArray[x], (0, 0), None, scale, scale)
            else:
                imgArray[x] = cv2.resize(imgArray[x], (imgArray[0].shape[1], imgArray[0].shape[0]), None,scale, scale)
            if len(imgArray[x].shape) == 2: imgArray[x] = cv2.cvtColor(imgArray[x], cv2.COLOR_GRAY2BGR)
        hor= np.hstack(imgArray)
        ver = hor
    return ver

while True:
    success, img = cap.read()   # While another frame exists, read it
    img = cv2.resize(img, (imageWidth, imageHeight))    # Resize image
    imgContour = img.copy()                         # Create copy

    imgThreshold = preProcessing(img)
    biggest = getContours(imgThreshold)

    if biggest.size != 0:
        imgWarped = getWarp(img, biggest)
        imageArray = ([img, imgThreshold],
                    [imgContour, imgWarped])
        cv2.imshow("ImageWarped", imgWarped)
    else:
        imageArray = ([img, imgThreshold],
                      [img, img])

    stackedImages = stackImages(0.6, imageArray)
    cv2.imshow("Workflow", stackedImages)

    if cv2.waitKey(1) & 0xFF == ord('q'):   # If 'q' is pressed, end video
        break