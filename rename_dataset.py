import json
import os
import argparse


def change_names(dataset, start, extension):
    cnt = start
    for image in dataset['images']:
        new_name = "{}.{}".format(cnt, extension)
        os.rename(image['file_name'], new_name)
        image['file_name'] = new_name
        image['flickr_url'] = new_name
        image['coco_url'] = new_name
        cnt += 1
    return dataset


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--json_path",
        required=True,
        help="path to annotation file",
    )
    parser.add_argument(
        "--start",
        default=0,
        type=int,
        help="rename the images with a counter, which begins with start",
    )
    parser.add_argument(
        "--extension",
        default="png",
        choices=['png','jpg','bmp'],
        help="file extension of the images: png, jpg...",
    )
    parser.add_argument(
        "--output",
        default="new_dataset.json",
        help="name for the new cleaned dataset",
    )

    args = parser.parse_args()
    images_path = "/".join(args.json_path.split("/")[:-1])
    os.chdir(images_path)

    with open(args.json_path) as file:
        dataset = json.load(file)

    new_dataset = change_names(dataset, args.start, args.extension)

    with open(args.output, 'w') as out_file:
        json.dump(new_dataset, out_file)


if __name__ == "__main__":
    main()
