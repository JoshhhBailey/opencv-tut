# CHAPTER 2 - Basic Processing of Images

import cv2
import numpy as np

img = cv2.imread("Assets/diana.jpeg")   # Read image
kernel = np.ones((5, 5), np.uint8)      # 5x5 Matrix

imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)                 # Convert to grayscale
imgBlur = cv2.GaussianBlur(imgGray, (7, 7), 0)                  # Blur image
imgCanny = cv2.Canny(img, 150, 150)                             # Detect edges
imgDialation = cv2.dilate(imgCanny, kernel, iterations = 1)     # Dilate edges
imgEroded = cv2.erode(imgDialation, kernel, iterations = 1)     # Erode edges

# Show images
cv2.imshow("Gray Image", imgGray)
cv2.imshow("Blur Image", imgBlur)
cv2.imshow("Canny Image", imgCanny)
cv2.imshow("Dialation Image", imgDialation)
cv2.imshow("Erosion Image", imgEroded)

cv2.waitKey(0)  # Hold image