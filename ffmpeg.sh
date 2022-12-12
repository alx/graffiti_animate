#!/usr/bin/env sh

ffmpeg -y -f image2 -i index_%05d.png -vcodec libx264 -crf 25 output.mp4
