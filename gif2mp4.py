#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import os.path
import re
import subprocess
import sys

devnull = open('/dev/null', 'w')

def convert(file,overwrite=False,keep=True):
    if not file.endswith('.gif'):
        return
    base_name = file[:-4]
    target = base_name + ".mp4"
    if os.path.exists(target) and not overwrite:
        return
    duration = get_duration(file)
    frame_count = get_frame_count(file)
    if not frame_count:
        return
    if not duration:
        frame_rate = 5
    else:
        frame_rate = frame_count/duration
    cmd("ffmpeg -v quiet -r " + str(frame_rate) + " -i  " + file + " -crf 20 -tune film -preset veryslow -y -an " + target)
    if not keep:
        os.system("rm " + file)

def cmd(cmd):
    os.system(cmd)

def get_duration(file):
    args = [ "exiftool", "-Duration", file ]
    output = subprocess.check_output(args, stderr=devnull)
    match = re.search(r'^Duration                        : (\d+.\d+) s\n$', output)
    if match:
        return float(match.group(1))
    else:
        return None

def get_frame_count(file):
    args = [ "exiftool", "-FrameCount", file ]
    output = subprocess.check_output(args, stderr=devnull)
    match = re.search(r'Frame Count                     : (\d+)\n$', output)
    if match:
        return int(match.group(1))
    else:
        return None

if __name__ == '__main__':
    for file in sys.argv[1:]:
        convert(file)