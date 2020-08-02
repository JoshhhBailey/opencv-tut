# CHAPTER 4 - Shapes and Text

import cv2
import numpy as np

img = np.zeros((512, 512, 3), np.uint8)  # 512 x 512 matrix of 0's (black), 3 channels
#print(img)
#img[:] = 255, 0, 0             # Turn matrix blue (BGR)

cv2.line(img, (0, 0), (img.shape[1], img.shape[0]), (0, 255, 0), 3)     # Draw line
cv2.rectangle(img, (0, 0), (250, 350), (0, 0, 255), 2)                  # Draw rectangle
cv2.circle(img, (400, 50), 30, (255, 255, 0), 5)                        # Draw circle
cv2.putText(img, " OPENCV ", (300, 200), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 150, 0), 1)   # Draw text

cv2.imshow("Image", img)

cv2.waitKey(0)