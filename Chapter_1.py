# CHAPTER 1 - Read Images, Videos and Webcams

import cv2
print("Using OpenCV version {0}".format(cv2.__version__))

frameWidth = 640
frameHeight = 480

'''
# Image
img = cv2.imread("Assets/diana.jpeg")     # Read image
cv2.imshow("Output", img)                 # Show image
cv2.waitKey(0)                            # Hold image
'''

'''
# Video
cap = cv2.VideoCapture("Assets/falcon.mp4")   # Read video

while True:
    success, img = cap.read()                 # While another frame exists, read it
    cv2.imshow("Video", img)                  # Show frame

    if cv2.waitKey(1) & 0xFF == ord('q'):     # If 'q' is pressed, end video
        break
'''

# Webcam - Must execute through terminal, not VS Code
cap = cv2.VideoCapture(1)   # Get webcam, 0 = default id
cap.set(3, frameWidth)      # Define width
cap.set(4, frameHeight)     # Define height

while True:
    success, img = cap.read()   # While another frame exists, read it
    cv2.imshow("Video", img)    # Show frame

    if cv2.waitKey(1) & 0xFF == ord('q'):   # If 'q' is pressed, end video
        break