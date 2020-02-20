import cv2
import numpy as np
import pickle

# Rectangular kernel for eroding and dilating the mask
kernel = np.ones((7, 7), np.uint8)

# Default colour ranges
blue_range = np.array([[88, 78, 20], [128, 255, 255]])
yellow_range = np.array([[21, 70, 80], [61, 255, 255]])
red_range = np.array([[158, 85, 72], [180, 255, 255]])


# 'nothing' function is useful when creating track_bars
def nothing(x):
    pass


def calibrate_color(color, col_range):
    name = 'Calibrate ' + color
    cv2.namedWindow(name)
    cv2.createTrackbar('Hue', name, col_range[0][0], 255, nothing)
    cv2.createTrackbar('Sat', name, col_range[0][1], 255, nothing)
    cv2.createTrackbar('Val', name, col_range[0][2], 255, nothing)
    while True:
        _, img = cap.read()
        img = cv2.flip(img, 1)
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        hue = cv2.getTrackbarPos('Hue', name)
        sat = cv2.getTrackbarPos('Sat', name)
        val = cv2.getTrackbarPos('Val', name)

        lower = np.array([hue - 20, sat, val])
        upper = np.array([hue + 20, 255, 255])

        mask = cv2.inRange(hsv, lower, upper)
        eroded = cv2.erode(mask, kernel, iterations=1)
        dilated = cv2.dilate(eroded, kernel, iterations=1)
        cv2.imshow(name, dilated)

        key = cv2.waitKey(5) & 0xFF
        if key == ord('s'):
            cv2.destroyWindow(name)
            return np.array([[hue - 20, sat, val], [hue + 20, 255, 255]])

        elif key == ord('d'):
            cv2.destroyWindow(name)
            return col_range


def get_trackbar_values(range_filter):
    values = []
    for i in range_filter:
        for j in i:
            values.append(int(j))
    return values


def change_status(key):
    global red_range, yellow_range, blue_range

    if key == ord('r'):
        print('----------------------------------------------------------------------')
        print('You have entered calibration mode.')
        print('calibrate the color you want to use   1.RED   2.YELLOW   3.BLUE')
        print('press D to set the color to default value or skip')
        print('Use the track_bars to calibrate and press S when done.')
        print('----------------------------------------------------------------------')
        red_range = calibrate_color('Red', red_range)
        yellow_range = calibrate_color('Yellow', yellow_range)
        blue_range = calibrate_color('Blue', blue_range)
        print('	Calibration Successful')
        print('----------------------------------------------------------------------')
        print('Press R to recalibrate color ranges.')
        print("choose One colors to use:   1.Red as'R'   2.Yellow as'Y'   3.BLue as'B'")
        print('Press ESC to exit.')
        print('----------------------------------------------------------------------')

    else:
        pass


cap = cv2.VideoCapture(0)

print('----------------------------------------------------------------------')
print('You have entered calibration mode.')
print('calibrate the color you want to use   1.RED   2.YELLOW   3.BLUE')
print('press D to set the color to default value or skip')
print('Use the track_bars to calibrate and press S when done.')
print('----------------------------------------------------------------------')

red_range = calibrate_color('Red', red_range)
yellow_range = calibrate_color('Yellow', yellow_range)
blue_range = calibrate_color('Blue', blue_range)
print('	Calibration Successful')

cv2.namedWindow('Frame')
print('----------------------------------------------------------------------')
print('Press R to recalibrate color ranges.')
print("choose One colors to use:   1.Red as'X'   2.Yellow as'Y'   3.BLue as'Z'")
print('Press ESC to exit.')
print('----------------------------------------------------------------------')

while True:
    k = cv2.waitKey(10) & 0xFF
    change_status(k)
    ret, image = cap.read()
    image = cv2.flip(image, 1)
    cv2.imshow('Frame', image)

    v1_min, v2_min, v3_min, v1_max, v2_max, v3_max = get_trackbar_values(red_range)
    x = (v1_min, v2_min, v3_min, v1_max, v2_max, v3_max)

    v1_min, v2_min, v3_min, v1_max, v2_max, v3_max = get_trackbar_values(yellow_range)
    y = (v1_min, v2_min, v3_min, v1_max, v2_max, v3_max)

    v1_min, v2_min, v3_min, v1_max, v2_max, v3_max = get_trackbar_values(blue_range)
    z = (v1_min, v2_min, v3_min, v1_max, v2_max, v3_max)

    with open("range.pickle", "wb") as f:
        if k == ord('x'):
            pickle.dump(x, f)
            break
        elif k == ord('y'):
            pickle.dump(y, f)
            break
        elif k == ord('z'):
            pickle.dump(z, f)
            break
        elif k == 27:
            break

f.close()
cap.release()
cv2.destroyAllWindows()
