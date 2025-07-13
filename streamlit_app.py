import streamlit as st
import cv2
import numpy as np
import tempfile
import os

st.set_page_config(page_title="Green Screen Video App", layout="centered")
st.title("🎬 Green Screen Video Replacement App")

st.markdown("Upload a green screen video and a background video to replace the green screen background.")

# Upload videos
bg_video = st.file_uploader("Upload Background Video", type=["mp4", "mov"], key="bg_vid")
fg_video = st.file_uploader("Upload Foreground Video (with green screen)", type=["mp4", "mov"], key="fg_vid")

if bg_video and fg_video:
    st.video(fg_video)
    st.video(bg_video)

    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as bg_temp, \
         tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as fg_temp, \
         tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as out_temp:

        # Save uploaded videos to temp files
        bg_temp.write(bg_video.read())
        fg_temp.write(fg_video.read())

        bg_path = bg_temp.name
        fg_path = fg_temp.name
        out_path = out_temp.name

        # Load videos
        fg_cap = cv2.VideoCapture(fg_path)
        bg_cap = cv2.VideoCapture(bg_path)

        # Get video properties
        width = int(fg_cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(fg_cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = fg_cap.get(cv2.CAP_PROP_FPS)

        # Output writer
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out_writer = cv2.VideoWriter(out_path, fourcc, fps, (width, height))

        # Process frames
        while True:
            ret_fg, fg_frame = fg_cap.read()
            ret_bg, bg_frame = bg_cap.read()

            if not ret_fg or not ret_bg:
                break

            bg_frame = cv2.resize(bg_frame, (width, height))

            hsv = cv2.cvtColor(fg_frame, cv2.COLOR_BGR2HSV)
            lower_green = np.array([35, 40, 40])
            upper_green = np.array([85, 255, 255])
            mask = cv2.inRange(hsv, lower_green, upper_green)
            mask_inv = cv2.bitwise_not(mask)

            fg_part = cv2.bitwise_and(fg_frame, fg_frame, mask=mask_inv)
            bg_part = cv2.bitwise_and(bg_frame, bg_frame, mask=mask)
            combined = cv2.add(fg_part, bg_part)

            out_writer.write(combined)

        fg_cap.release()
        bg_cap.release()
        out_writer.release()

        st.success("✅ Green screen replacement complete!")
        st.video(out_path)

        # Cleanup optional
        # os.remove(bg_path)
        # os.remove(fg_path)
