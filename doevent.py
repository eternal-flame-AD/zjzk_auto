import random
import subprocess

def drift():
    return random.uniform(10,30)

def tap(px,py,need_resize,width,height):
    if need_resize:
        px*=width
        py*=height
    si = subprocess.STARTUPINFO()
    si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    cmd = 'adb shell input tap {x} {y}'.format(
        x=px,
        y=py
    )
    subprocess.Popen(cmd, startupinfo=si)