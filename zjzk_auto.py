import ctypes
#import os
import sys
import time
#import math
import random
import subprocess
from PIL import Image
from common import screenshot
import eventparser
import doevent

def do_screenshot():
    global need_resize,need_rotate,height,width
    print("Pull_screenshot...",end=" ")
    screenshot.pull_screenshot()
    try:
        im = Image.open('./autojump.png')
        success=True
    except:
        success=False
        try:
            screenshot.pull_screenshot()
            im = Image.open('./autojump.png')
            success=True
        except:
            print("screenshot_error")
    if success:
        if need_rotate:
            print("Rotating...",end=" ")
            im=im.transpose(Image.ROTATE_90)
            width=width+height
            height=width-height
            width=width-height
        if need_resize:
            print("Resizing...",end=" ")
            im=im.resize((1080,1920))
    return im

def init():
    global height,width,need_resize,need_rotate
    screenshot.check_screenshot()
    screenshot.pull_screenshot()
    im = Image.open('./autojump.png')
    width,height=im.size
    need_rotate=False
    need_resize=False
    if width<height:
            print("Need rotate!")
            need_rotate=True
            im=im.transpose(Image.ROTATE_90)
            width=width+height
            height=width-height
            width=width-height
    if (width!=1920) or (height!=1080):
            print("Need resize!")
            need_resize=True
    im.close()
    width=width/1920
    height=height/1080

def main():
    init()
    im=do_screenshot()
    print(eventparser.in_challenge_selection(im))
    
main()