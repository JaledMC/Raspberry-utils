# VIDEO UTILS




## USAGE

### `crop_video.py`:

Use this script to crop a video in equal length videos

```bash
python crop_video --file <VideoFile> --split_size <Seconds>
# e.g. Crop video1.mp4 in 1 minute videos
python crop_video --file video1.mp4 --split_size 60
```

### `download_videos_youtube.py`:

Use this script to download a list of videos from youtube.

```bash
python download_videos_youtube.py --links_file <LinksFile>
# e.g. Download videos from youtubeLinks.txt
python download_videos_youtube.py  --links_file youtubeLinks.txt
```

**Note the file containing the links should have one link per line, as follows:**

```html
https://www.youtube.com/watch?v=XqZsoesa55w
https://www.youtube.com/watch?v=020g-0hhCAU
https://www.youtube.com/watch?v=FX20kcp7j5c
```



