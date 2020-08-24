"""Crop a folder of images given their YOLO annotations"

from glob import glob
import cv2


def read_annotations(filename):
    with open(filename, 'r') as f:
        return f.readlines()


def anno2num(annotations):
    num_annotations = []
    for annotation in annotations:
        print("annotation 2 num: {}".format(annotation))
        label, x, y, w, h = annotation.split(" ")
        num_annotations.append((int(label), float(x), float(y), float(w), float(h)))
    return num_annotations


def yolo2bbox(annotation):
    print(type(annotation))
    label, x, y, w, h = annotation
    xmin = x - w/2
    xmax = x + w/2
    ymin = y - h/2
    ymax = y + h/2
    return label, xmin, ymin, xmax, ymax


def rel2abs(image, bbox):
    _, xmin, ymin, xmax, ymax = bbox
    h, w, _ = image.shape
    xmin = int(xmin * w)
    xmax = int(xmax * w)
    ymin = int(ymin * h)
    ymax = int(ymax * h)
    return xmin, ymin, xmax, ymax


def crop_image(image, annotation, offset):
    bbox = yolo2bbox(annotation)
    xmin, ymin, xmax, ymax = rel2abs(image, bbox)
    h, w, _ = image.shape
    ymin_offset = (ymin-offset) if (ymin-offset) > 0 else 0
    ymax_offset = (ymax+offset) if (ymax+offset) < h else h 
    xmin_offset = (xmin-offset) if (xmin-offset) > 0 else 0
    xmax_offset = (xmax+offset) if (xmax+offset) < w else w
    return image[ymin_offset:ymax_offset, xmin_offset:xmax_offset, :], bbox[0]


if __name__ == "__main__":
    for image_txt in glob("*.txt"):
        image_name = image_txt.replace("txt", "jpg")
        image = cv2.imread(image_name)
        annotations = read_annotations(image_txt)
        annotations = anno2num(annotations)
        cnt = 0
        for annotation in annotations:
            cropped_image, label = crop_image(image, annotation, 25)
            cv2.imwrite("{}_{}_{}".format(label, cnt, image_name), cropped_image)
            cnt += 1
