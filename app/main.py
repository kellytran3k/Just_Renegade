import pose_analyze as pa
import cv2
import numpy as np
import base64
import time
import sys
from selenium import webdriver
import os

driver = webdriver.Chrome()
driver.get("file:///{}".format(os.path.abspath("index.html")))

target_fps = 20
frame_time = 1 / target_fps

debug = True
if not debug:
    sys.path.append("../../openpose/")

def resize(img, scale):
    width = int(img.shape[1] * scale)
    height = int(img.shape[0] * scale)
    dim = (width, height)

    return cv2.resize(img, dim, interpolation = cv2.INTER_AREA)

def resize_match(img1, img2):
    h1 = img1.shape[0]
    h2 = img2.shape[0]

    scale = h2 / h1

    return resize(img1, scale)

def op_analyze(img):
    return img

def send(message):
    print(message)
    sys.stdout.flush()

def send_img(img):
    _, buffer = cv2.imencode('.png', img)
    content = buffer.tobytes()
    img_code = base64.b64encode(content).decode('ascii')
    
    send(img_code)

def start_game(video_file):
    cam = cv2.VideoCapture(0)

    video = cv2.VideoCapture(video_file)
    video_fps = video.get(cv2.CAP_PROP_FPS)

    current_video_frame = 0
    video_to_target_ratio = int(video_fps / target_fps)
    
    last = time.time()

    while video.isOpened():
        success, vframe = video.read()

        if not success:
            break

        _, user_cam = cam.read()
        user_cam = resize(user_cam, 0.5)
        user_cam = cv2.flip(user_cam, 1)

        vframe = resize_match(vframe, user_cam)

        w = user_cam.shape[1] + vframe.shape[1]
        wd = w - user_cam.shape[1]
        h = user_cam.shape[0]
        stitch = np.zeros((h, w, 3), np.uint8)

        stitch[0:vframe.shape[0], 0:vframe.shape[1]] = vframe
        stitch[0:vframe.shape[0], wd:w] = user_cam

        #stitch[0:h, 0:w] = user_cam

        send_img(stitch)

        elapsed = time.time() - last
        frames_to_skip = elapsed * video_fps

        for i in range(0, int(frames_to_skip)):
            success, img = video.read()

            if not success:
                break
        
        last = time.time()

        # time.sleep(frame_time)
    
    cam.release()
    video.release()

#start_game("/Users/kphan/trishRenegadeVid.mov")