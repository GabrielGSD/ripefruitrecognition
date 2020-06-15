import numpy as np
import cv2

cap = cv2.VideoCapture(1)

def nothing(x):
    pass

img = np.zeros((300,512,3), np.uint8)
cv2.namedWindow('image')

# create trackbars for color change
cv2.createTrackbar('H','image',0,179,nothing)
cv2.createTrackbar('S','image',0,255,nothing)
cv2.createTrackbar('V','image',0,255,nothing)

cv2.createTrackbar('H2','image',0,179,nothing)
cv2.createTrackbar('S2','image',0,255,nothing)
cv2.createTrackbar('V2','image',0,255,nothing)


while 1:
    _, frame = cap.read()
    hsvImage = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    h = cv2.getTrackbarPos('H','image')
    s = cv2.getTrackbarPos('S','image')
    v = cv2.getTrackbarPos('V','image')

    h2 = cv2.getTrackbarPos('H2','image')
    s2 = cv2.getTrackbarPos('S2','image')
    v2 = cv2.getTrackbarPos('V2','image')

    lower = np.array((h, s, v))
    upper = np.array((h2, s2, v2))

    print("lower ", h, s, v)
    print("upper ", h2, s2, v2)

    mask = cv2.inRange(hsvImage, lower, upper)

    result = cv2.bitwise_and(frame, frame, mask=mask)

    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    if contours:
        maxArea = cv2.contourArea(contours[0])
        contourId = 0
        i = 0
        for cnt in contours:
            if maxArea < cv2.contourArea(cnt):
                maxArea = cv2.contourArea(cnt)
                contourId = i
            i += 1
        cnt = contours[contourId]
        x, y, w, h = cv2.boundingRect(contours[contourId])
        
        if maxArea > 100.0:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 3)

    cv2.imshow('frame', frame)
    cv2.imshow('result', result)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()