#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import sys

def convert(file):
    if not file.endswith('.gif'):
        return
    base_name = file[:-4]
    duration = get_duration(file)
    frame_count = get_frame_count(file)
    if not duration:
        frame_rate = 5
    else:
        frame_rate = frame_count/duration
    cmd("ffmpeg -v quiet -r " + str(frame_rate) + " -i  " + file + " -y -an " + base_name + ".mp4")

def cmd(cmd):
    os.system(cmd)

def get_duration(file):
    output = os.popen("exiftool -Duration " + file).read()
    match = re.search(r'^Duration                        : (\d+.\d+) s\n$', output)
    if match:
        return float(match.group(1))
    else:
        return None

def get_frame_count(file):
    output = os.popen("exiftool -FrameCount " + file).read()
    match = re.search(r'Frame Count                     : (\d+)\n$', output)
    if match:
        return int(match.group(1))
    else:
        return None

if __name__ == '__main__':
    for file in sys.argv[1:]:
        convert(file)