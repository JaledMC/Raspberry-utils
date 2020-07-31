import cv2
from chessCalibrate import calculate_matrix

points = []


def button_call(event, x, y, flags, param):
    global points
    if event == cv2.EVENT_LBUTTONDBLCLK:
        if len(points) == 1:
            points.append((x, y))
            print("X pixels: ",  abs(points[0][0] - points[1][0]))
            print("Y pixels: ", abs(points[0][1] - points[1][1]))
        else:
            points = [(x, y)]


def drawing(image, points, color=(255, 0, 0), thick=10):
    for point in points:
        cv2.circle(image, point, thick, color, -1)
    if len(points) == 2:
        cv2.line(image, points[0], points[1], color, thick)
    return image


def setup_matrix(path, image):
    ret, mtx, dist, rvecs, tvecs = calculate_matrix(path)
    h,  w = image.shape[:2]
    newcameramtx, roi = cv2.getOptimalNewCameraMatrix(mtx, dist, (w, h), 1, (w, h))
    return newcameramtx, roi, mtx, dist


def undistort(frame, newcameramtx, roi, mtx, dist):
    dst = cv2.undistort(frame, mtx, dist, None, newcameramtx)
    x, y, w, h = roi
    return dst[y:y+h, x:x+w]


def main():
    src = cv2.VideoCapture(2)
    cv2.namedWindow('frame')
    cv2.setMouseCallback('frame', button_call)
    _, frame = src.read()
    newcameramtx, roi, mtx, dist = setup_matrix("CornersDetected", frame)
    while True:
        ret, frame = src.read()
        frame = undistort(frame, newcameramtx, roi, mtx, dist)
        frame = drawing(frame, points)
        cv2.imshow('frame', frame)
        key = cv2.waitKey(20)
        if key == 27:  # Esc key to exit
            break
    src.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
