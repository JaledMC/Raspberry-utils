# FFMPEG

`FFMPEG` commands to achieve a bunch of different things.

## EXTRACT FRAMES FROM VIDEO

Extract frames from video. If you want to extract less frames, just put a bigger `-r` number in the first `-r`

```bash
# Extract all frames from video
ffmpeg -r 1 -i <input_video> -r 1 "$filename%03d.png
# Exctract a frame per second aprox (depends on video bitrate, try to adjust the first -r number to adjust it to your needs). The bigger the -r, the less frames extracted
ffmpeg -r 20 -i <input_video> -r 1 "$filename%03d.png
```



## REDUCE VIDEO SIZE

Reduce video size retaining the quality as much as possible. `--crf` refers to *Constant Rate Factor* and can vary around 18 and 24. The lower the `--crf` the highest the bitrate (bigger size).

```bash
ffmpeg -i <input_video> -vcodec libx264 -crf 20 <output_video>
# e.g. Reduce the size as much as possible of video1.mp4
ffmpeg -i video1.mp4 -vcodec libx264 -crf 24 video1_output.mp4
```



# REFERENCES

[1] https://unix.stackexchange.com/questions/28803/how-can-i-reduce-a-videos-size-with-ffmpeg