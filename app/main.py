import pose_analyze as pa
import cv2
import numpy as np
import base64
import time
import sys
from selenium import webdriver
import os
import subprocess
import pygame

video_path = os.path.abspath("app/just_renegade.mp4")
audio_folder_path = os.path.abspath("app/cache/")
audio_path = os.path.abspath("app/cache/audio.wav")

if not os.path.exists(audio_path):
    os.mkdir(audio_folder_path)

if os.path.exists(audio_path):
    os.remove(audio_path)

command = "ffmpeg -i {} -ab 160k -ac 2 -ar 44100 -vn {}".format(video_path, audio_path)
subprocess.call(command, shell=True)

pygame.init()
current_audio = None

driver = webdriver.Chrome()
driver.get("file:///{}".format(os.path.abspath("app/index.html")))

target_fps = 20
frame_time = 1 / target_fps

debug = True
if not debug:
    sys.path.append("../../openpose/")

def playSound(filename):
    global current_audio

    if current_audio is None:
        current_audio = pygame.mixer.Sound(audio_path)
        current_audio.play()

def resize(img, scale):
    width = int(img.shape[1] * scale)
    height = int(img.shape[0] * scale)
    dim = (width, height)

    return cv2.resize(img, dim, interpolation = cv2.INTER_AREA)

def resize_match_width(img, width):
    scale = width / img.shape[1]

    return resize(img, scale)

def resize_match_height(img, height):
    scale = height / img.shape[0]

    return resize(img, scale)

def op_analyze(img):
    return img

def execute(command):
    driver.execute_script(command)

def send_img(img):
    _, buffer = cv2.imencode('.png', img)
    content = buffer.tobytes()
    img_code = base64.b64encode(content).decode('ascii')
    
    execute('''document.getElementById('viewport').setAttribute('src', 'data:image/png;base64,{}');'''.format(img_code))

def set_viewport(visible):
    execute("document.getElementById('viewport').style.visibility = '{}'".format(visible))

def start_game(video_file):
    set_viewport("block")

    video = cv2.VideoCapture(video_file)
    video_fps = video.get(cv2.CAP_PROP_FPS)
    frame_time = 1 / video_fps
    
    last = time.time()

    while video.isOpened():
        success, vframe = video.read()

        if not success:
            break

        vframe = resize_match_height(vframe, 720)

        playSound(audio_path)
        send_img(vframe)

        elapsed = time.time() - last
        frames_to_skip = elapsed * video_fps

        for i in range(0, int(frames_to_skip) - 1):
            success, img = video.read()

            if not success:
                break
        
        last = time.time()

        # time.sleep(frame_time)
    
    video.release()
    end_game()

def end_game():
    global current_audio

    print("HIDE")
    current_audio.stop()
    current_audio = None
    set_viewport("none")
    execute("resetPage()")

while True:
    input = driver.find_element_by_id("sel-in").get_attribute("textContent")

    if input:
        print("Received from JS: {}".format(input))
        execute('document.getElementById("sel-in").innerHTML = ""')

        start_game(video_path)
    
    time.sleep(0.1)
