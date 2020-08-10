import cv2


def nothing(x):
    pass


cap = cv2.VideoCapture(2)

# Create a window
cv2.namedWindow('frame')

# create trackbars
cv2.createTrackbar('brightness', 'frame', 0, 100, nothing)
cv2.createTrackbar('contrast', 'frame', 0, 100, nothing)
cv2.createTrackbar('saturacion', 'frame', 0, 100, nothing)
cv2.createTrackbar('exposure', 'frame', 0, 100, nothing)
cap.set(cv2.CAP_PROP_FPS, 5)

frame_width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
frame_height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
brightness = cap.get(cv2.CAP_PROP_BRIGHTNESS)
contrast = cap.get(cv2.CAP_PROP_CONTRAST)
saturacion = cap.get(cv2.CAP_PROP_SATURATION)
exposure = cap.get(cv2.CAP_PROP_EXPOSURE)
fps = cap.get(cv2.CAP_PROP_FPS)

print("frame_width: " + str(frame_width))
print("frame_height: " + str(frame_height))
print("fps: " + str(fps))
print("brightness: " + str(brightness))
print("contrast: " + str(contrast))
print("saturacion: " + str(saturacion))
print("exposure: " + str(exposure))

while(True):
    # get value trackbar
    fps = cv2.getTrackbarPos("fps", "frame")
    brightness = cv2.getTrackbarPos("brightness", "frame")
    contrast = cv2.getTrackbarPos("contrast", "frame")
    saturacion = cv2.getTrackbarPos("saturacion", "frame")
    exposure = cv2.getTrackbarPos("exposure", "frame")

    # set properties webcam
    cap.set(cv2.CAP_PROP_BRIGHTNESS, brightness/100)
    cap.set(cv2.CAP_PROP_CONTRAST, contrast/100)
    cap.set(cv2.CAP_PROP_SATURATION, saturacion/100)
    cap.set(cv2.CAP_PROP_EXPOSURE, exposure/100)

    ret, frame = cap.read()
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) == 27:
        break
cap.release()
cv2.destroyAllWindows()
