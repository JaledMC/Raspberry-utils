import json
import glob
import os
import cv2
import numpy as np

"""
    Script to change a class value for another in all images
    of the dataset, either semantic or via format
"""


def parse_options():
    parser = argparse.ArgumentParser()
    parser.add_option(
        "-f", "--format",
        choices=['via', 'semantic'],
        help="dataset format. VIA or semantic",

    )
    parser.add_option(
        "-p", "--path",
        help="path to via file or semantic images folder",
        )
    parser.add_option(
        "--old_class",
        help="value of the class to be changed",
    )
    parser.add_option(
        "--new_class",
        help="new value for the class",
    )
    return parser.parse_args()


def remove_via_class(region):
    if region["region_attributes"]["class"] == old_class:
        return False
    else:
        return True


def main():
    args = parse_options()
    if args.format == "via":
        with open("args.path", "r") as file:
            dataset = json.load(file)
        for name, image in dataset.items():
            image["regions"] = [region for region in image["regions"] if remove_via_class(region)]
        with open("args.path".replace(".json", "_removed.json"), 'w') as out_file:
            json.dump(dataset, out_file)
    else:
        os.chdir(args.path)
        for image_name in glob.glob("*.png"):
            image = cv2.imread(image_name)
            image[image == args.old_class] = args.new_class
            cv2.imwrite(image_name, image)


if __name__ == "__main__":
    main()
