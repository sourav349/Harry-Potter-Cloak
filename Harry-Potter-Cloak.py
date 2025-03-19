import cv2
import numpy as np

# Initial function for the calling of the trackbar
def hello(x):
    pass  # No need for print(""), use 'pass' instead

# Initialization of the camera
cap = cv2.VideoCapture(0)
bars = cv2.namedWindow("bars")

cv2.createTrackbar("upper_hue", "bars", 110, 180, hello)
cv2.createTrackbar("upper_saturation", "bars", 255, 255, hello)
cv2.createTrackbar("upper_value", "bars", 255, 255, hello)
cv2.createTrackbar("lower_hue", "bars", 68, 180, hello)
cv2.createTrackbar("lower_saturation", "bars", 55, 255, hello)
cv2.createTrackbar("lower_value", "bars", 54, 255, hello)

# Capturing the initial frame for creation of background
while True:
    cv2.waitKey(1000)
    ret, init_frame = cap.read()
    if ret:
        break

# Create a full-screen window.................................
cv2.namedWindow("Harry's Cloak", cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty("Harry's Cloak", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

# Start capturing the frames for actual magic
while True:
    ret, frame = cap.read()
    if not ret:
        break

    inspect = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Getting the HSV values for masking the cloak
    upper_hue = cv2.getTrackbarPos("upper_hue", "bars")
    upper_saturation = cv2.getTrackbarPos("upper_saturation", "bars")
    upper_value = cv2.getTrackbarPos("upper_value", "bars")
    lower_hue = cv2.getTrackbarPos("lower_hue", "bars")
    lower_saturation = cv2.getTrackbarPos("lower_saturation", "bars")
    lower_value = cv2.getTrackbarPos("lower_value", "bars")

    # Kernel to be used for dilation
    kernel = np.ones((3, 3), np.uint8)

    upper_hsv = np.array([upper_hue, upper_saturation, upper_value])
    lower_hsv = np.array([lower_hue, lower_saturation, lower_value])

    mask = cv2.inRange(inspect, lower_hsv, upper_hsv)
    mask = cv2.medianBlur(mask, 3)
    mask_inv = 255 - mask
    mask = cv2.dilate(mask, kernel, 5)

    # Mixing frames in a combination to achieve the required frame
    frame_inv = cv2.bitwise_and(frame, frame, mask=mask_inv)
    blanket_area = cv2.bitwise_and(init_frame, init_frame, mask=mask)

    final = cv2.addWeighted(frame_inv, 1, blanket_area, 1, 0)

    cv2.imshow("Harry's Cloak", final)

    if cv2.waitKey(3) == ord('q'):
        break

cv2.destroyAllWindows()
cap.release()
