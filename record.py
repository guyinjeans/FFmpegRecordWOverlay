#!/bin/python3.6

import os
import sys
import signal
import time

from subprocess import *

import ffmpy

videoSizeX = '1366'
videoSizeY = '768'
videoSize = videoSizeX + 'x' + videoSizeY

home = os.path.expanduser('~')
dirPath = home + '/Recordings/'
dir = os.path.dirname(dirPath)

TIMESTAMP = time.strftime('%Y%m%d-%H%M%S')

DISP = str(os.environ['DISPLAY'])

STR_USAGE = """
Usage of \'record\' is as follows:       

    record start 
    record stop 
"""

STR_RUNNING = "FFmpeg seems to already be running on Process "

try:
    os.stat(dir)
except:
    print('Directory not found. Creating directory at: ' + home + dirPath)
    os.mkdir(dir)

if len(sys.argv) == 1:
    print(STR_USAGE)
    sys.exit()

if len(sys.argv) > 2:
    print('Too many arguments!')
    print(STR_USAGE)
    sys.exit()

try:
    pids = list(map(int,(check_output(['pidof', 'ffmpeg'])).split()))
    running = True
except:
    running = False

ffScreenWithOverlay = ffmpy.FFmpeg(
    inputs={ DISP + '.0':'-video_size '+videoSize+' -f x11grab', '/dev/video0': '-f v4l2 -video_size 320x180', 'default':'-f  pulse -ac 2'},
    outputs={dir+'/REC-' + TIMESTAMP + '.mkv': ['-filter_complex',"overlay=main_w-overlay_w-10:main_h-overlay_h-10"]}
)

if(sys.argv[1] == 'start'):
    if(running):
        for pid in pids:
            print(STR_RUNNING + str(pid))
        sys.exit()
    else:
        print(ffScreenWithOverlay.cmd)
        ffScreenWithOverlay.run()
        sys.exit()
elif(sys.argv[1] == 'stop'):
    if(running):
        for pid in pids:
            print('Jsyk, I\'m killin\' this thing at ' + str(pid))
            os.kill(pid, signal.SIGINT)
        sys.exit()
    else:
        print('You don\'t seem to have started recording yet?')
        sys.exit()
else:
    print('This doesn\'t seem to be a valid command. See usage for more details:')
    print(STR_USAGE)
    sys.exit()
