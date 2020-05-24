import glob
import argparse
import shutil
import os


def parse_options():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-s", "--src",
        help="path to original image folder",
        )
    parser.add_argument(
        "-d", "--dst",
        help="path for moving images",
        )
    return parser.parse_args()


def move_images(src_path, dst_path):
    """
    Move images to selected folder if it has been yolo annotated
    """
    os.chdir(src_path)
    annotations = glob.glob("*.txt")
    images = [name.replace(".txt", ".jpg") for name in annotations]
    for image in images:
        shutil.move("{}/{}".format(src_path, image), "{}/{}".format(dst_path, image))


def main():
    args = parse_options()
    move_images(args.src, args.dst)


if __name__ == "__main__":
    main()
