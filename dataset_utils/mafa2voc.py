from scipy.io import loadmat
import os
import cv2


def annotation2voc(image_name, annotations):
    voc_annotations = []
    for annotation in annotations:
        x = annotation[0]
        y = annotation[1]
        w = annotation[2]
        h = annotation[3]
        label = annotation[12]
        x, y, w, h = bbox_format(image_name, x, y, w, h)
        voc_annotations.append((label, x, y, w, h))
    return voc_annotations


def txt_name(image_name):
    return image_name.split(".")[0] + ".txt"


def bbox_format(name, x, y, w, h):
    image = cv2.imread(name)
    height, width, _ = image.shape
    x = (x + w/2)/width
    y = (y + h/2)/height
    w = w/width
    h = h/height
    return x, y, w, h


def image2txt(name, voc_annotations):
    name = txt_name(name)
    with open(name, 'w') as f:
        for annotation in voc_annotations:
            label, x, y, w, h = annotation
            f.write("{} {} {} {} {}\n".format(label, x, y, w, h))


def main():
    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    train = open("train.txt", "w")
    dataset = loadmat('LabelTrainAll.mat')['label_train'][0][:30]
    for annotations in dataset:
        image_name = annotations[1][0]
        voc_annotations = annotation2voc(image_name, annotations[2])
        image2txt(image_name, voc_annotations)
        train.write(txt_name(image_name) + "\n")
    train.close()


if __name__ == "__main__":
    main()
