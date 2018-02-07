import random
import subprocess
import eventparser
import time

def drift():
    return random.uniform(10,30)

def tap(px,py,need_resize=False,width=1,height=1,debug=False):
    if need_resize:
        px*=width
        py*=height
    si = subprocess.STARTUPINFO()
    si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    cmd = 'adb shell input tap {x} {y}'.format(
        x=int(px),
        y=int(py)
    )
    if debug:
        print(cmd)
    subprocess.Popen(cmd, startupinfo=si)

def swipe(px,py,deltax,time=1000,need_resize=False,width=1,height=1,debug=False):
    #input swipe <x1> <y1> <x2> <y2>
    if need_resize:
        px*=width
        py*=height
        deltax*=width
    si = subprocess.STARTUPINFO()
    si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    cmd = 'adb shell input swipe {x} {y} {x1} {y} {t}'.format(
        x=int(px),
        x1=int(px+deltax),
        y=int(py),
        t=time
    )
    if debug:
        print(cmd)
    subprocess.Popen(cmd, startupinfo=si)

def rematch():
    tap(1192+drift(),873+drift())

def enter_mode_selection():
    tap(1743+drift(),901+drift())

def select_mode(x):
    if x==1:
        tap(354+drift(),325+drift())
    elif x==2:
        tap(714+drift(),337+drift())
    elif x==3:
        tap(1122+drift(),337+drift())
    elif x==4:
        tap(1488+drift(),447+drift())
    else:
        raise RuntimeError("Illegal mode!")

def select_challenge_1(x):
    if x==1:
        tap(732+drift(),942+drift())
    elif x==2:
        tap(915+drift(),942+drift())
    elif x==3:
        tap(1096+drift(),942+drift())
    else:
        raise RuntimeError('Illegal challgenge 1')

def select_challenge_2(x):
    swipe(100,300+drift(),1000)
    time.sleep(5)
    tap(175*x-53+drift(),277+drift())
    time.sleep(2)
    if x>4:
        swipe(1800,300+drift(),-1000)
        time.sleep(3)

def start_challenge(im):
    x,y=eventparser.find_start_button(im)
    tap(x,y)

def anykey():
    tap(random.uniform(100,1000),random.uniform(100,1000))

def go_back():
    tap(1612+drift(),871+drift())

def start_war():
    tap(1768+drift(),894+drift())
