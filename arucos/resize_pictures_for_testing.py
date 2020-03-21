import argparse
import cv2


def parser():
    # process input options
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--path',
        help='Path to image',
        required=True,
        type=str
        )
    parser.add_argument(
        '--scale_percent',
        help='Percentage to scale',
        required=True,
        type=int
        )
    return parser.parse_args()


args = parser()
img = cv2.imread(args.path, cv2.IMREAD_UNCHANGED)
print('Original Dimensions : ', img.shape)
width = int(img.shape[1] * args.scale_percent / 100)
height = int(img.shape[0] * args.scale_percent / 100)
resized = cv2.resize(img, (width, height), interpolation=cv2.INTER_AREA)
print('Resized Dimensions : ', resized.shape)
cv2.imwrite('resized.jpg', resized)
