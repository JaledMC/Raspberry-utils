import argparse
import numpy as np
import cv2
import cv2.aruco as aruco
import matplotlib.pyplot as plt
import matplotlib as mpl


def parser():
    # process input options
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--id',
        help='Aruco ID',
        default=1,
        type=int
        )
    parser.add_argument(
        '--quantity',
        help='Quantity of arucos to create',
        default=1,
        type=int
        )
    parser.add_argument(
        '--format',
        help='Format to save arucos (.jpg or .pdf)',
        default='jpg',
        type=str
        )
    return parser.parse_args()


'''
Create ARUCO
ARUCO DICTIONARY: Check dictionaries for reference:
https://docs.opencv.org/trunk/d9/d6a/group__aruco.html#ggac84398a9ed9dd01306592dd616c2c975a6eb1a3e9c94c7123d8b1904a57193f16
'''

args = parser()
aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_250)
# second parameter is id number
# last parameter is total image size
# drawMarker(dictionary, ID, sidePixel)
if (args.format == 'jpg'):
    for i in range(args.quantity):
        img = aruco.drawMarker(aruco_dict, args.id + i, 700)
        cv2.imwrite("aruco_id{}.jpg".format(args.id + i), img)
        cv2.imshow('frame', img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
else:
    for i in range(args.quantity):  # ID
        fig = plt.figure()
        img = aruco.drawMarker(aruco_dict, args.id + i, 700)
        plt.imshow(img, cmap=mpl.cm.gray, interpolation="nearest")
        plt.axis("off")
        plt.savefig("aruco_id{}.pdf".format(args.id + i))
        plt.show()
