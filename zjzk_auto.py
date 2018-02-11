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
import intmenu

def dump_eventparser(im):
    print("================================")
    print('walkshop: ',eventparser.find_walkshop(im))
    print('loading: ',eventparser.in_loading_screen(im))
    print('in_main: ',eventparser.in_main(im))
    print('in_benzhen: ',eventparser.in_benzhen(im))
    print('in_war: ',eventparser.in_fight(im))
    print('win_presplash: ',eventparser.in_win_presplash(im))
    print('win_presplash_ready: ',eventparser.win_presplash_ready(im))
    print('win_splash: ',eventparser.in_win_splash(im))
    print('win_type: ',eventparser.determine_win_type(im))
    print('mode_selection: ',eventparser.in_mode_selection(im))
    print('challenge_selection: ',eventparser.in_challenge_selection(im))
    print('player_selection: ',eventparser.in_player_selection(im))
    print("================================")

def do_screenshot():
    global need_resize,need_rotate,want_main_menu
    try:
        im = screenshot.pull_screenshot()
        success=True
    except KeyboardInterrupt:
        want_main_menu=True
        im = screenshot.pull_screenshot()
        success=True
    except:
        print("Fail fallback...")
        success=False
        try:
            im = Image.open('./autojump.png')
            success=True
        except KeyboardInterrupt:
            want_main_menu=True
        except:
            im=do_screenshot()
    if success:
        if need_rotate:
            print("Rotating...",end=" ")
            im=im.transpose(Image.ROTATE_90)
        if need_resize:
            print("Resizing...",end=" ")
            im=im.resize((1080,1920))
    return im

def init():
    global height,width,need_resize,need_rotate
    screenshot.check_screenshot()
    im=screenshot.pull_screenshot()
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
            raise RuntimeError("ERR: Unsupported resolution, pls use 1920x1080")
            print("Need resize!")
            need_resize=True
    im.close()
    width=width/1920
    height=height/1080

def validchal(mode,chal1,chal2):
    if mode==1:
        return (chal1 in range(1,4) and chal2 in range(1,8))
    elif mode==2:
        return (chal1 in range(1,4) and chal2 in range(1,8))
    elif mode==3:
        return (chal2 in range(1,11))
    elif mode==4:
        return (chal1 in range(1,5) and chal2 in range(1,11))
    return False

def ask_chal():
    mode=0
    chal1=0
    chal2=0
    while not(validchal(mode,chal1,chal2)):
        mode=int(input("mode?"))
        if mode!=3:
            chal1=int(input("challenge_1?"))
        chal2=int(input("challenge_2?"))
    print("ACCEPTED")
    return mode,chal1,chal2

def main():
    want_main_menu=False
    debug=False
    softchange=False
    init()
    if not eventparser.tess_init():
        print("Tesseract INIT failed!")
        print("NO LEVEL DETECTION support!")
        level_detection_on=False
    else:
        level_detection_on=True
    im=do_screenshot()
    im.save("temp.png")
    dump_eventparser(im)
    mode,chal1,chal2=ask_chal()
    max_full_level_count=int(input('Max full level count?'))
    chal1_selected=False
    chal2_selected=False
    failcount=0
    while True:
        try:
            im=do_screenshot()
            if debug:
                dump_eventparser(im)
            if eventparser.in_fight(im):
                pass
            elif eventparser.in_loading_screen(im):
                pass
            elif eventparser.in_benzhen(im):
                doevent.enter_mode_selection()
            elif eventparser.in_main(im):
                doevent.enter_mode_selection()
            elif eventparser.in_mode_selection(im):
                softchange=False
                chal1_selected=False
                chal2_selected=False
                doevent.select_mode(mode)
            elif eventparser.in_challenge_selection(im):
                if not chal1_selected:
                    chal1_selected=True
                    doevent.select_challenge_1(chal1,mode)
                elif not chal2_selected:
                    chal2_selected=True
                    doevent.select_challenge_2(chal2)
                else:
                    doevent.start_challenge(im)
            elif eventparser.in_win_presplash(im):
                if eventparser.win_presplash_ready(im):
                    if level_detection_on:
                        result=eventparser.parse_level(im)
                        if result==-1:
                            print("Failed to locate player...Retrying next time")
                        else:
                            print(result,'Full level count:',eventparser.max_full_count(result))
                            if eventparser.max_full_count(result)>max_full_level_count:
                                raise SystemExit("Full Level count threshold reached, Stopping...")
                    doevent.anykey()
            elif eventparser.in_win_splash(im):
                x=eventparser.determine_win_type(im)
                if eventparser.find_walkshop(im):
                    print("walkshop")
                if softchange or (x==2):
                    doevent.go_back()
                elif x==1:
                    doevent.enter_somethinghappened()
                elif x==0:
                    doevent.rematch()
            elif eventparser.in_player_selection(im):
                doevent.start_war()
            else:
                failcount+=1
                #print("Failed parse. Count=",failcount)
                if failcount==20:
                    dump_eventparser(im)
                    im.close()
                    raise RuntimeError("Failed to parse image!!!")
                else:
                    continue
            failcount=0
            im.close()
            time.sleep(1)
            if want_main_menu:
                want_main_menu=False
                raise KeyboardInterrupt
        except KeyboardInterrupt:
            op=intmenu.show_menu()
            if op==1:
                raise SystemExit("bye...")
            elif op==2:
                print("Change will take place in next battle.")
                mode,chal1,chal2=ask_chal()
                chal1_selected=False
                chal2_selected=False
                softchange=True
            elif op==4:
                do_screenshot().save('screenshot.png')
                print("screenshot taken")
        continue
main()