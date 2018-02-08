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
    tap(1030+drift(),873+drift())

def enter_mode_selection():
    tap(1743+drift(),901+drift())

def select_mode(x):
    if x==1:
        tap(100+drift(),325+drift())
    elif x==2:
        tap(474+drift(),337+drift())
    elif x==3:
        tap(846+drift(),337+drift())
    elif x==4:
        tap(1240+drift(),447+drift())
    else:
        raise RuntimeError("Illegal mode!")

def select_challenge_1(x,mode):
    if (mode==1 or mode==2):
        if x==1:
            tap(732+drift(),942+drift())
        elif x==2:
            tap(915+drift(),942+drift())
        elif x==3:
            tap(1096+drift(),942+drift())
        else:
            raise RuntimeError('Illegal challgenge 1')
    elif mode==4:
        if x==1:
            tap(661+drift(),977+drift())
        elif x==2:
            tap(837+drift(),967+drift())
        elif x==3:
            tap(1025+drift(),976+drift())
        elif x==4:
            tap(1201+drift(),986+drift())
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
    tap(x+drift(),y+drift())

def anykey():
    tap(random.uniform(100,1000),random.uniform(100,1000))

def go_back():
    tap(1612+drift(),871+drift())

def start_war():
    tap(1768+drift(),894+drift())
