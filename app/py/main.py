import pose_analyze as pa
import cv2
import numpy as np
import base64
import time
import sys

debug = True
if not debug:
    sys.path.append("../../openpose/")

def resize(img, scale):
    width = int(img.shape[1] * scale)
    height = int(img.shape[0] * scale)
    dim = (width, height)

    return cv2.resize(img, dim, interpolation = cv2.INTER_AREA)

def op_analyze(img):
    return img

def send(message):
    print(message)
    sys.stdout.flush()

cam = cv2.VideoCapture(0)

while True:
    _, img = cam.read()
    img = resize(img, 0.25)
    img = cv2.flip(img, 1)

    # run image through openpose
    img = op_analyze(img)

    _, buffer = cv2.imencode('.png', img)
    content = buffer.tobytes()
    img_code = base64.b64encode(content).decode('ascii')
    
    send(img_code)

    # cap at 20
    time.sleep(1 / 20)

cam.release()