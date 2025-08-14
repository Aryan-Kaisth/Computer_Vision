"""
🎯 Webcam HSV Color Tracker with Live Contours

This script:
- Lets you select a color range in HSV space using trackbars.
- Tracks objects in that color range using contours.
- Draws bounding boxes and center points on detected objects.
- Shows a live color preview of the detected object.
- Press 's' to save a snapshot of the detection.
- Press ESC to exit.
"""

import cv2 as cv
import numpy as np
import time

# Open webcam
cap = cv.VideoCapture(0)

def nothing(x):
    pass

# Create window for trackbars
cv.namedWindow("Color_Adjustments")

# HSV Trackbars
cv.createTrackbar("Lower_H", "Color_Adjustments", 0,   179, nothing)
cv.createTrackbar("Lower_S", "Color_Adjustments", 0,   255, nothing)
cv.createTrackbar("Lower_V", "Color_Adjustments", 0,   255, nothing)
cv.createTrackbar("Upper_H", "Color_Adjustments", 179, 179, nothing)
cv.createTrackbar("Upper_S", "Color_Adjustments", 255, 255, nothing)
cv.createTrackbar("Upper_V", "Color_Adjustments", 255, 255, nothing)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv.resize(frame, (640, 480))
    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

    # Get trackbar positions
    Lower_H = cv.getTrackbarPos("Lower_H", "Color_Adjustments")
    Lower_S = cv.getTrackbarPos("Lower_S", "Color_Adjustments")
    Lower_V = cv.getTrackbarPos("Lower_V", "Color_Adjustments")
    Upper_H = cv.getTrackbarPos("Upper_H", "Color_Adjustments")
    Upper_S = cv.getTrackbarPos("Upper_S", "Color_Adjustments")
    Upper_V = cv.getTrackbarPos("Upper_V", "Color_Adjustments")

    lower_limit = np.array([Lower_H, Lower_S, Lower_V])
    upper_limit = np.array([Upper_H, Upper_S, Upper_V])

    # Create mask and result
    mask = cv.inRange(hsv, lower_limit, upper_limit)
    result = cv.bitwise_and(frame, frame, mask=mask)

    # Find contours on mask
    contours, _ = cv.findContours(mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

    for cnt in contours:
        area = cv.contourArea(cnt)
        if area > 800:  # filter small noise
            x, y, w, h = cv.boundingRect(cnt)
            cx, cy = x + w // 2, y + h // 2  # center point

            # Draw bounding box & center
            cv.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv.circle(frame, (cx, cy), 5, (0, 0, 255), -1)

            # Show live color preview
            color_preview = frame[y:y+h, x:x+w]
            if color_preview.size > 0:
                avg_color = color_preview.mean(axis=(0, 1)).astype(int)
                cv.rectangle(frame, (10, 10), (110, 60),
                             tuple(int(c) for c in avg_color), -1)
                cv.putText(frame, f"Color", (15, 50),
                           cv.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

    # Show windows
    cv.imshow("Original with Tracking", frame)
    cv.imshow("Mask", mask)
    cv.imshow("Result", result)

    # Save snapshot
    key = cv.waitKey(1) & 0xFF
    if key == ord('s'):
        filename = f"snapshot_{int(time.time())}.png"
        cv.imwrite(filename, frame)
        print(f"Saved snapshot: {filename}")

    # Exit on ESC
    elif key == 27:
        break

cap.release()
cv.destroyAllWindows()
