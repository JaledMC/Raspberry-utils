import argparse
import numpy as np
import cv2
import PIL
from cv2 import aruco
import matplotlib.pyplot as plt
import matplotlib as mpl
import pandas as pd


def parser():
    # process input options
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--aruco_path',
        help='Path to aruco image',
        required=True,
        type=str
        )
    return parser.parse_args()


'''
Create ARUCO
ARUCO DICTIONARY: Check dictionaries for reference:
https://docs.opencv.org/trunk/d9/d6a/group__aruco.html#ggac84398a9ed9dd01306592dd616c2c975a6eb1a3e9c94c7123d8b1904a57193f16
'''

args = parser()
frame = cv2.imread(args.aruco_path)
gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_250)
parameters = aruco.DetectorParameters_create()
corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, aruco_dict, parameters=parameters)
frame_markers = aruco.drawDetectedMarkers(frame.copy(), corners, ids)

plt.figure()
plt.imshow(cv2.cvtColor(frame_markers, cv2.COLOR_BGR2RGB))
if hasattr(ids, 'any'):
    for i in range(len(ids)):
        c = corners[i][0]
        plt.plot([c[:, 0].mean()], [c[:, 1].mean()], "o", label="id={0}".format(ids[i]))
    plt.legend()
    plt.show()
else:
    print("Didn't find any ARUCO.")
