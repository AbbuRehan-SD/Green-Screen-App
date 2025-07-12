import cv2
import numpy as np
import os

def remove_green_screen(fg_path, bg_path):
    print("DEBUG: Foreground path:", fg_path)
    print("DEBUG: Background path:", bg_path)

    if not os.path.exists(fg_path) or not os.path.exists(bg_path):
        raise FileNotFoundError("Foreground or background image path is invalid.")

    fg_img = cv2.imread(fg_path)
    bg_img = cv2.imread(bg_path)

    if fg_img is None:
        raise ValueError("Foreground image could not be loaded. Check the file format or path.")
    if bg_img is None:
        raise ValueError("Background image could not be loaded. Check the file format or path.")

    fg_img = cv2.resize(fg_img, (bg_img.shape[1], bg_img.shape[0]))
    hsv = cv2.cvtColor(fg_img, cv2.COLOR_BGR2HSV)

    lower_green = np.array([35, 40, 40])
    upper_green = np.array([85, 255, 255])
    mask = cv2.inRange(hsv, lower_green, upper_green)

    mask_inv = cv2.bitwise_not(mask)
    fg_masked = cv2.bitwise_and(fg_img, fg_img, mask=mask_inv)
    bg_masked = cv2.bitwise_and(bg_img, bg_img, mask=mask)

    final = cv2.add(fg_masked, bg_masked)
    return final
