'''
Script to download videos from youtube given a
text file containing youtube links (one link per line).
'''

from __future__ import unicode_literals
import argparse
import  copy
import youtube_dl


def parser():
    # process input options
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--links_file",
        type=str,
        help="Youtube List of links to download",
        required=True
        )
    return parser.parse_args()


def main():
    args = parser()
    ydl_opts = {}
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        file1 = open(args.links_file, 'r')
        videos = file1.readlines()
        videos_copy = copy.deepcopy(videos)
        for video in videos:
            ydl.download([video])
            videos_copy.remove(video)
            print(videos_copy)


if __name__ == "__main__":
    main()
    print("Finished downloads.")
