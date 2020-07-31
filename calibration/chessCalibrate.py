"""
https://docs.opencv.org/master/dc/dbb/tutorial_py_calibration.html
"""
import numpy as np
import cv2
import os
import glob


def save_images(src, path):
    if not os.path.exists(path):
        os.makedirs(path)
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
    cnt = 1
    while True:
        ret, frame = src.read()
        cv2.imshow('frame', frame)
        key = cv2.waitKey(1)
        if key == 27:  # Esc key to exit
            break
        if key == ord('s'):
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            ret, corners = cv2.findChessboardCorners(gray, (7, 6), None)
            if ret:
                fine_corners = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
                detection = frame.copy()
                cv2.drawChessboardCorners(detection, (7, 6), fine_corners, ret)
                cv2.imshow('Corners', detection)
                cv2.imwrite("{}/Chess{}.jpg".format(path, cnt), frame)
                print("{} images saved".format(cnt))
                cnt += 1
    src.release()
    cv2.destroyAllWindows()


def calculate_matrix(path):
    # termination criteria
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
    # prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
    objp = np.zeros((6*7, 3), np.float32)
    objp[:, :2] = np.mgrid[0:7, 0:6].T.reshape(-1, 2)
    # Arrays to store object points and image points from all the images.
    objpoints = []  # 3d point in real world space
    imgpoints = []  # 2d points in image plane.
    images = glob.glob("{}/*.jpg".format(path))
    for fname in images:
        img = cv2.imread(fname)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # Find the chess board corners
        ret, corners = cv2.findChessboardCorners(gray, (7, 6), None)
        # If found, add object points, image points (after refining them)
        if ret:
            fine_corners = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
            imgpoints.append(corners)
            objpoints.append(objp)
    return cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)


def undistort(src, mtx, dist):
    ret, frame = src.read()
    h,  w = frame.shape[:2]
    newcameramtx, roi = cv2.getOptimalNewCameraMatrix(mtx, dist, (w, h), 1, (w, h))
    while True:
        ret, frame = src.read()
        dst = cv2.undistort(frame, mtx, dist, None, newcameramtx)
        x, y, w, h = roi
        dst = dst[y:y+h, x:x+w]
        cv2.imshow('frame', dst)
        key = cv2.waitKey(1)
        if key == 27:  # Esc key to exit
            break
    src.release()
    cv2.destroyAllWindows()


def main():
    cap = cv2.VideoCapture(2)
    folder_name = "CornersDetected"
    save_images(cap, folder_name)
    ret, mtx, dist, rvecs, tvecs = calculate_matrix(folder_name)
    undistort(cap, mtx, dist)


if __name__ == "__main__":
    main()
