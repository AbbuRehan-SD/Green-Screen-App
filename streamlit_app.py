import streamlit as st
import numpy as np
import cv2
from PIL import Image
import tempfile
import os

st.set_page_config(page_title="Green Screen Replacement", layout="wide")

st.markdown("<h1 style='text-align: center;'>🌿 Green Screen Replacement</h1>", unsafe_allow_html=True)

st.markdown("### Upload Background Image")
bg_image = st.file_uploader("Drag and drop file here", type=["png", "jpg", "jpeg"], key="bg_img")

st.markdown("### Upload Foreground Image (green screen)")
fg_image = st.file_uploader("Drag and drop file here", type=["png", "jpg", "jpeg"], key="fg_img")

if bg_image and fg_image:
    bg = Image.open(bg_image).convert("RGB")
    fg = Image.open(fg_image).convert("RGB")

    bg = bg.resize(fg.size)

    fg_np = np.array(fg)
    bg_np = np.array(bg)

    hsv = cv2.cvtColor(fg_np, cv2.COLOR_RGB2HSV)
    lower_green = np.array([35, 40, 40])
    upper_green = np.array([85, 255, 255])
    mask = cv2.inRange(hsv, lower_green, upper_green)
    mask_inv = cv2.bitwise_not(mask)

    fg_clean = cv2.bitwise_and(fg_np, fg_np, mask=mask_inv)
    bg_part = cv2.bitwise_and(bg_np, bg_np, mask=mask)
    final_img = cv2.add(fg_clean, bg_part)

    st.image(final_img, caption="🖼️ Final Output Image", use_column_width=True)

# -------------------------------
# 🎥 Green Screen Video Section
# -------------------------------

st.markdown("## 🎥 Green Screen Video Replacement")
bg_video = st.file_uploader("Upload Background Video", type=["mp4", "mov"], key="bg_vid")
fg_video = st.file_uploader("Upload Foreground Video (with green screen)", type=["mp4", "mov"], key="fg_vid")

def process_green_screen_video(foreground_path, background_path, output_path):
    fg_cap = cv2.VideoCapture(foreground_path)
    bg_cap = cv2.VideoCapture(background_path)

    width = int(fg_cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(fg_cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(fg_cap.get(cv2.CAP_PROP_FPS))

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    while fg_cap.isOpened() and bg_cap.isOpened():
        ret_fg, frame_fg = fg_cap.read()
        ret_bg, frame_bg = bg_cap.read()

        if not ret_fg or not ret_bg:
            break

        frame_bg = cv2.resize(frame_bg, (width, height))

        hsv = cv2.cvtColor(frame_fg, cv2.COLOR_BGR2HSV)
        lower_green = np.array([35, 40, 40])
        upper_green = np.array([85, 255, 255])
        mask = cv2.inRange(hsv, lower_green, upper_green)
        mask_inv = cv2.bitwise_not(mask)

        fg_clean = cv2.bitwise_and(frame_fg, frame_fg, mask=mask_inv)
        bg_part = cv2.bitwise_and(frame_bg, frame_bg, mask=mask)
        combined = cv2.add(fg_clean, bg_part)

        out.write(combined)

    fg_cap.release()
    bg_cap.release()
    out.release()

if bg_video and fg_video:
    st.video(bg_video)
    st.video(fg_video)

    if st.button("🎬 Process Video"):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as fg_tmp, tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as bg_tmp:
            fg_tmp.write(fg_video.read())
            fg_path = fg_tmp.name

            bg_tmp.write(bg_video.read())
            bg_path = bg_tmp.name

        output_path = "processed_output.mp4"
        process_green_screen_video(fg_path, bg_path, output_path)

        st.success("✅ Video processed successfully!")
        st.video(output_path)
