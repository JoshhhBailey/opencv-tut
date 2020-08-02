import cv2

frameWidth = 640
frameHeight = 480
numberPlateCascade = cv2.CascadeClassifier("Assets/haarcascade_russian_plate_number.xml")
minArea = 500
color = (255, 0, 255)
count = 0

cap = cv2.VideoCapture(1)   # Get webcam, 0 = default id
cap.set(3, frameWidth)      # Define width
cap.set(4, frameHeight)     # Define height

while True:
    success, img = cap.read()   # While another frame exists, read it
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)         # Convert to grayscale

    numberPlates = numberPlateCascade.detectMultiScale(imgGray, 1.5, 5)   # Detect number plates

    for (x, y, w, h) in numberPlates:
        area = w * h

        if area > minArea:
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 255), 2)  # Draw bounding box around number plate
            cv2.putText(img, "Number Plate",(x, y - 5),                   # Draw text
                        cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, color, 2)
            imgRoi = img[y:y + h, x:x + w]                                # Region of number plate
            cv2.imshow("ROI", imgRoi)
    
    cv2.imshow("Result", img)    # Show frame

    if cv2.waitKey(1) & 0xFF == ord('s'):   # If 's' is pressed, save number plate
        cv2.imwrite("Assets/Scanned_Number_Plates/NoPlate" + str(count) + ".jpg", imgRoi)
        cv2.rectangle(img, (0, 200), (640, 300), (0, 255, 0), cv2.FILLED)
        cv2.putText(img, "Scan Saved", (150, 265),
                    cv2.FONT_HERSHEY_DUPLEX,2, (0, 0, 255), 2)

        cv2.imshow("Result", img)
        cv2.waitKey(500)
        count += 1

    if cv2.waitKey(1) & 0xFF == ord('q'):   # If 'q' is pressed, end video
        break