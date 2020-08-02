# CHAPTER 9 - Face Detection

import cv2

faceCascade = cv2.CascadeClassifier("Assets/haarcascade_frontalface_default.xml")
img = cv2.imread("Assets/group.jpeg")
imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)         # Convert to grayscale

faces = faceCascade.detectMultiScale(imgGray, 1.5, 5)   # Detect faces

for (x, y, w, h) in faces:
    cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)  # Draw bounding box around face


cv2.imshow("Result", img)
cv2.waitKey(0)