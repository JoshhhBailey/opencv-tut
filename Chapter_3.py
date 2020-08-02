# CHAPTER 3 - Resizing and Cropping

import cv2
import numpy as np

img = cv2.imread("Assets/diana.jpeg")
print(img.shape)                            # Print image size = height, width, depth

imgResize = cv2.resize(img, (400, 300))     # Resize image, height then width
print(img.shape)

imgCropped = img[0:200, 200:500]            # Crop image, height then width

cv2.imshow("Image", img)
cv2.imshow("Image Resize", imgResize)
cv2.imshow("Image Cropped", imgCropped)

cv2.waitKey(0)