"""
    This script shows one by one each image within a folder, by natural order,
    and save selected ones typing "s" key in "selected" folder
"""


import cv2
import glob
import os
from natsort import natsorted
import argparse


parser = argparse.ArgumentParser()
parser.add_argument(
    '-images_path',
    type=str,
    help='path to folder with images to be detected')
parser.add_argument(
    '--scale',
    type=int,
    default=3,
    help='Downscale the image for better visualization. Doesnt change saved image')


def main():
    args = parser.parse_args()
    os.chdir(args.images_path)
    os.mkdir("selected")

    images = glob.glob('*.jpg') + glob.glob('*.jpeg') + glob.glob('*.png')
    images = natsorted(images)

    cnt = 0
    for image_name in images:
        image = cv2.imread(image_name)
        resized_image = cv2.resize(image, (image.shape[1]//args.scale, image.shape[0]//args.scale))

        cv2.imshow('image', resized_image)
        k = cv2.waitKey(0)
        cnt += 1
        if k == 27:  # wait for ESC to stop the program
            cv2.destroyAllWindows()
            break
        elif k == ord('s'):  # wait for 's' key to save and exit
            cv2.imwrite('selected/{}.png'.format(cnt), image)
            cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
