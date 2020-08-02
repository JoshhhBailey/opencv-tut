# CHAPTER 5 - Warp Perspective

import cv2
import numpy as np

img = cv2.imread("Assets/cards.jpeg")

width, height = 250, 350    # Playing card 2.5" x 3.5"
pts1 = np.float32([[368, 686], [885, 586], [493, 1455], [1073, 1328]])  # Matrix of warp points
pts2 = np.float32([[0, 0], [width, 0], [0, height], [width, height]])   # TopL, TopR, BottomL, BottomR
matrix = cv2.getPerspectiveTransform(pts1, pts2)                        # Get transformation matrix
imgOutput = cv2.warpPerspective(img, matrix, (width, height))           # Warp image

cv2.imshow("Image", img)
cv2.imshow("Output", imgOutput)

cv2.waitKey(0)