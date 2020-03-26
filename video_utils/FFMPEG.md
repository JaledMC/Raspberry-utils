# FFMPEG

FFMPEG commands to achieve a bunch of different things.

## REDUCE VIDEO SIZE

Reduce video size retaining the quality as much as possible. `--crf` refers to *Constant Rate Factor* and can vary around 18 and 24. The lower the `--crf` the highest the bitrate (bigger size).

```bash
ffmpeg -i <input_video> -vcodec libx264 -crf 20 <output_video>
# e.g. Reduce the size as much as possible of video1.mp4
ffmpeg -i video1.mp4 -vcodec libx264 -crf 24 video1_output.mp4
```



# REFERENCES

[1] https://unix.stackexchange.com/questions/28803/how-can-i-reduce-a-videos-size-with-ffmpeg