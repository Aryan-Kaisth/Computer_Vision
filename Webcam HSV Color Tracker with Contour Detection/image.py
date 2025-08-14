"""
🎨 HSV Color Filtering with an Image

This script loads a static image and allows you to interactively
filter specific colors using HSV (Hue, Saturation, Value) sliders.

Move the trackbars to adjust the lower and upper HSV bounds, and watch:
    - "mask" → shows only pixels in the selected HSV range (white = in range)
    - "result" → shows the original image but with only the selected color visible

Press ESC to exit.
"""

import cv2 as cv
import numpy as np

# Load image and resize
img = cv.imread(r"C:\AI Pwskill\daily\src\colors.jpg")
img = cv.resize(src=img, dsize=(600, 400))

# Callback for trackbars (required even if it does nothing)
def nothing(x):
    pass

# Create window for trackbars
cv.namedWindow("Color_Adjustments")

# Hue ranges 0–179; Saturation & Value range 0–255
cv.createTrackbar("Lower_H", "Color_Adjustments", 0,   179, nothing)
cv.createTrackbar("Lower_S", "Color_Adjustments", 0,   255, nothing)
cv.createTrackbar("Lower_V", "Color_Adjustments", 0,   255, nothing)
cv.createTrackbar("Upper_H", "Color_Adjustments", 179, 179, nothing)
cv.createTrackbar("Upper_S", "Color_Adjustments", 255, 255, nothing)
cv.createTrackbar("Upper_V", "Color_Adjustments", 255, 255, nothing)

while True:
    # Convert to HSV color space
    hsv = cv.cvtColor(src=img, code=cv.COLOR_BGR2HSV)

    # Read current slider values
    Lower_H = cv.getTrackbarPos("Lower_H", "Color_Adjustments")
    Lower_S = cv.getTrackbarPos("Lower_S", "Color_Adjustments")
    Lower_V = cv.getTrackbarPos("Lower_V", "Color_Adjustments")
    Upper_H = cv.getTrackbarPos("Upper_H", "Color_Adjustments")
    Upper_S = cv.getTrackbarPos("Upper_S", "Color_Adjustments")
    Upper_V = cv.getTrackbarPos("Upper_V", "Color_Adjustments")

    # Define lower & upper HSV limits
    lower_limit = np.array([Lower_H, Lower_S, Lower_V])
    upper_limit = np.array([Upper_H, Upper_S, Upper_V])

    # Create mask: white = pixels within range
    mask = cv.inRange(hsv, lower_limit, upper_limit)

    # Apply mask to original image
    result = cv.bitwise_and(src1=img, src2=img, mask=mask)

    # Show results
    cv.imshow("original", img)
    cv.imshow("mask", mask)
    cv.imshow("result", result)

    # Exit if ESC is pressed
    if cv.waitKey(1) & 0xff == 27:
        break

cv.destroyAllWindows()
