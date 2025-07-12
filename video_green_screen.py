import cv2
import numpy as np
import os

def process_video(video_path, bg_path, output_path):
    print("[INFO] Starting video processing...")
    cap = cv2.VideoCapture(video_path)
    bg_img = cv2.imread(bg_path)

    if not cap.isOpened():
        print("[ERROR] Could not open video file.")
        return

    if bg_img is None:
        print("[ERROR] Background image failed to load.")
        return

    print("[INFO] Video and background loaded.")

    width  = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps    = int(cap.get(cv2.CAP_PROP_FPS))

    print(f"[INFO] Video size: {width}x{height} at {fps} FPS")

    bg_img = cv2.resize(bg_img, (width, height))

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    frame_count = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        lower_green = np.array([35, 40, 40])
        upper_green = np.array([85, 255, 255])
        mask = cv2.inRange(hsv, lower_green, upper_green)

        mask_inv = cv2.bitwise_not(mask)
        fg = cv2.bitwise_and(frame, frame, mask=mask_inv)
        bg = cv2.bitwise_and(bg_img, bg_img, mask=mask)

        combined = cv2.add(fg, bg)
        out.write(combined)

        frame_count += 1

    print(f"[INFO] Processed {frame_count} frames.")

    cap.release()
    out.release()
    print(f"[INFO] Output video saved to {output_path}")
