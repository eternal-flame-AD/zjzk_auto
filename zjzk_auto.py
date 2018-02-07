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

def dump_eventparser(im):
    print('walkshop: ',eventparser.find_walkshop(im))
    print('loading: ',eventparser.in_loading_screen(im))
    print('main: ',eventparser.in_main(im))
    print('in_war: ',eventparser.in_fight(im))
    print('win_presplash: ',eventparser.in_win_presplash(im))
    print('win_presplash_ready: ',eventparser.win_presplash_ready(im))
    print('win_splash: ',eventparser.in_win_splash(im))
    print('win_type: ',eventparser.determine_win_type(im))
    print('mode_selection: ',eventparser.in_mode_selection(im))
    print('challenge_selection: ',eventparser.in_challenge_selection(im))
    print('player_selection: ',eventparser.in_player_selection(im))

def do_screenshot():
    global need_resize,need_rotate,height,width
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
    debug=False
    init()
    im=do_screenshot()
    dump_eventparser(im)
    mode=int(input("mode(1-4)?"))
    chal1=int(input("challenge_1(1-3)?"))
    chal2=int(input("challenge_2(1-7)?"))
    chal1_selected=False
    chal2_selected=False
    failcount=0
    while True:
        im=do_screenshot()
        if debug:
            dump_eventparser(im)
        if eventparser.in_fight(im):
            if eventparser.find_walkshop(im):
                print("WALKSHOP!!!!!!")
        elif eventparser.in_loading_screen(im):
            continue
        elif eventparser.in_main(im):
            doevent.enter_mode_selection()
        elif eventparser.in_mode_selection(im):
            chal1_selected=False
            chal2_selected=False
            doevent.select_mode(mode)
        elif eventparser.in_challenge_selection(im):
            if not chal1_selected:
                chal1_selected=True
                doevent.select_challenge_1(chal1)
            elif not chal2_selected:
                chal2_selected=True
                doevent.select_challenge_2(chal2)
            else:
                doevent.start_challenge(im)
        elif eventparser.in_win_presplash(im):
            if eventparser.win_presplash_ready(im):
                doevent.anykey()
        elif eventparser.in_win_splash(im):
            x=eventparser.determine_win_type(im)
            if x==2:
                doevent.go_back()
            elif x>=0:
                doevent.rematch()
        elif eventparser.in_player_selection(im):
            doevent.start_war()
        else:
            failcount+=1
            if failcount==10:
                dump_eventparser(im)
                im.close()
                raise RuntimeError("Failed to parse image!!!")
            else:
                continue
        failcount=0
        im.close()
        time.sleep(1)
main()