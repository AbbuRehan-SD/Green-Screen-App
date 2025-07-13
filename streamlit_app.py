import streamlit as st
import cv2
import numpy as np
from PIL import Image

st.set_page_config(page_title="Green Screen App", layout="centered")

st.title("🌿 Green Screen Replacement")

# Upload background and foreground
bg_file = st.file_uploader("Upload Background Image", type=["png", "jpg"])
fg_file = st.file_uploader("Upload Foreground Image (green screen)", type=["png", "jpg"])

if bg_file and fg_file:
    bg = Image.open(bg_file).convert("RGB")
    fg = Image.open(fg_file).convert("RGB")

    bg = bg.resize(fg.size)
    bg_np = np.array(bg)
    fg_np = np.array(fg)

    # Create mask for green screen
    hsv = cv2.cvtColor(fg_np, cv2.COLOR_RGB2HSV)
    lower = np.array([35, 40, 40])
    upper = np.array([85, 255, 255])
    mask = cv2.inRange(hsv, lower, upper)
    mask_inv = cv2.bitwise_not(mask)

    fg_nobg = cv2.bitwise_and(fg_np, fg_np, mask=mask_inv)
    bg_only = cv2.bitwise_and(bg_np, bg_np, mask=mask)
    result = cv2.add(fg_nobg, bg_only)

    st.image(result, caption="🌄 Final Image", use_column_width=True)

    # Download button
    st.download_button(
        label="Download Image",
        data=cv2.imencode(".png", result)[1].tobytes(),
        file_name="green_screen_result.png",
        mime="image/png"
    )
