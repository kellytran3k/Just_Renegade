import pose_analyze as pa
import cv2
import numpy as np
import base64
import time
import sys

def resize(img, scale):
    width = int(img.shape[1] * scale)
    height = int(img.shape[0] * scale)
    dim = (width, height)

    return cv2.resize(img, dim, interpolation = cv2.INTER_AREA)

def send(message):
    print(message)
    sys.stdout.flush()

cam = cv2.VideoCapture(0)

while True:
    _, img = cam.read()
    img = resize(img, 0.25)
    img = cv2.flip(img, 1)
    _, buffer = cv2.imencode('.png', img)
    content = buffer.tobytes()
    img_code = base64.b64encode(content).decode('ascii')
    
    send(img_code)
    time.sleep(1 / 120)

cam.release()