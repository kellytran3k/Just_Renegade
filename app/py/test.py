import sys
import cv2
import os
from sys import platform
import argparse
import time
import numpy as np

openpose_python_mod = './openpose/build/python'
image_path = './test.png'

def resize(img, scale):
    width = int(img.shape[1] * scale)
    height = int(img.shape[0] * scale)
    dim = (width, height)

    return cv2.resize(img, dim, interpolation = cv2.INTER_AREA)

try:
    sys.path.append(openpose_python_mod);
    from openpose import pyopenpose as op

    # Custom Params (refer to include/openpose/flags.hpp for more parameters)
    params = dict()
    params["model_folder"] = "./openpose/models/"

    # Construct it from system arguments
    # op.init_argv(args[1])
    # oppython = op.OpenposePython()

    # Starting OpenPose
    opWrapper = op.WrapperPython()
    opWrapper.configure(params)
    opWrapper.start()

    # Grab image
    cam = cv2.VideoCapture(0)
    print("3")
    time.sleep(1)
    print("2")
    time.sleep(1)
    print("1")
    time.sleep(1)
    print("CHEESE")
    _, img = cam.read()


    print("3")
    time.sleep(1)
    print("2")
    time.sleep(1)
    print("1")
    time.sleep(1)
    print("CHEESE2")
    _, img2 = cam.read()
    print("done taking pics")

    begin = time.time()

    # Process Image
    datum = op.Datum()
    datum.cvInputData = img
    opWrapper.emplaceAndPop([datum])

    datum2 = op.Datum()
    datum.cvInputData = img2
    opWrapper.emplaceAndPop([datum])

    elapsed = time.time() - begin
    print("took {}".format(elapsed))

    # Display Image
    print("Body keypoints difference: \n" + str(np.subtract(datum2.poseKeypoints, datum.poseKeypoints)))
except Exception as e:
    print(e)
    sys.exit(-1)
