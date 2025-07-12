from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import os
import cv2
from green_screen import remove_green_screen
from video_green_screen import process_video

app = Flask(__name__)

# Folder paths
UPLOAD_FOLDER = 'static/uploads'
RESULT_FOLDER = 'static/results'
VIDEO_FOLDER = 'static/videos'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'mp4'}

# Ensure folders exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULT_FOLDER, exist_ok=True)
os.makedirs(VIDEO_FOLDER, exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    if request.method == 'POST':
        fg = request.files.get('foreground')
        bg = request.files.get('background')

        if fg and bg:
            fg_filename = secure_filename(fg.filename)
            bg_filename = secure_filename(bg.filename)

            fg_path = os.path.join(UPLOAD_FOLDER, fg_filename)
            bg_path = os.path.join(UPLOAD_FOLDER, bg_filename)

            fg.save(fg_path)
            bg.save(bg_path)

            result_img = remove_green_screen(fg_path, bg_path)

            result_path = os.path.join(RESULT_FOLDER, 'output.png')
            cv2.imwrite(result_path, result_img)

            result = '/' + result_path.replace('\\', '/')

    return render_template('index.html', result_image=result)

@app.route('/video', methods=['GET', 'POST'])
def video():
    result_video = None
    if request.method == 'POST':
        video = request.files.get('video')
        bg = request.files.get('background')

        if video and bg:
            video_filename = secure_filename(video.filename)
            bg_filename = secure_filename(bg.filename)

            video_path = os.path.join(UPLOAD_FOLDER, video_filename)
            bg_path = os.path.join(UPLOAD_FOLDER, bg_filename)

            video.save(video_path)
            bg.save(bg_path)

            output_path = os.path.join(VIDEO_FOLDER, 'output.mp4')
            process_video(video_path, bg_path, output_path)

            result_video = '/' + output_path.replace('\\', '/')

    return render_template('video.html', result_video=result_video)

import webbrowser
import threading

def open_browser():
    webbrowser.open_new("http://127.0.0.1:5000/")

if __name__ == '__main__':
    threading.Timer(1.0, open_browser).start()
    app.run(debug=False)

