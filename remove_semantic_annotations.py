import glob
import os
import cv2
import numpy as np

os.chdir("/home/ubuntu/image-segmentation-keras/test/varona4/train/wood_rind_knot/")
for file in glob.glob("*.png"):
    image = cv2.imread(file)
    image[image==4] = 1
    cv2.imwrite(file, image)
    print(np.unique(image))
