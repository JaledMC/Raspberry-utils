import glob
import os


def import_names():
    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    images = glob.glob("*.jpg") + glob.glob("*.jpeg") + glob.glob("*.png")
    return images


def create_train_file(names, file_name="train.txt"):
    with open(file_name, 'w') as f:
        for name in names:
            f.write(name + "\n")


def txt_name(image_name):
    return image_name.split(".")[0] + ".txt"


def image2txt(name):
    name = txt_name(name)
    with open(name, 'w') as f:
        f.write("")


def main():
    names = import_names()
    for name in names:
        image2txt(name)
    create_train_file(names)


if __name__ == "__main__":
    main()
