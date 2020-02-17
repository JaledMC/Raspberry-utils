# Raspberry-utils


## Camera

**WARNING!**  
The Pi captures video as a raw H264 video stream. Many media players will refuse to play it, or play it at an incorrect speed, unless it is "wrapped" in a suitable container format like MP4. The easiest way to obtain an MP4 file from the raspivid command is using MP4Box.

Install MP4Box with this command:
`sudo apt install -y gpac`

And convert the video with:
`MP4Box -add src.h264 dst.mp4`

**Specs**:
* Max birate is 25Mb/s
* With raspistill, at full resolution, 3280 x 2464 pixels, the speed is 1.3 fps. At 30fps, raspivid gives 1920x1080.
* Use -n for nonpreview
* A fast way to test some settings, is uses --demo. You can change parameters with `--save_settings`
* IP can be used
