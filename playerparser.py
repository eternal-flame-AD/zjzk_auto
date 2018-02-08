from PIL import Image
from eventparser import pixel_match
from tess import tess
import doevent
from common import screenshot

class name_parser:
    def __init__(self,im):
        self.im=im
    def parse(self,loc):
        x,y=loc
        '''
        fangang:
        95 1027
        59 42 27 @100 901
        127 1013 195 57 58
        '''
        if pixel_match(self.im,x+5,y-126,59,42,27,25) and pixel_match(self.im,x+32,y-14,189,58,59,15):
            return "fangang"
        '''
        mengxia:
        ref 273 1027
        '''
        if pixel_match(self.im,x-12,y-54,47,47,47,10) and pixel_match(self.im,x+97,y-19,27,45,63,20):
            return "mengxia"
        '''
        guangguo:
        ref 452 1027
        '''
        if pixel_match(self.im,x-23,y-102,203,176,104,20) and pixel_match(self.im,x+53,y-103,106,92,106,20):
            return "guangguo"
        '''
        xue(snow):
        ref 630 1027
        '''
        if pixel_match(self.im,x-4,y-106,229,229,226,15) and pixel_match(self.im,x+54,y-25,74,74,74,15):
            return "xue(snow)"
        '''
        bajiao
        ref 809 1027
        '''
        if pixel_match(self.im,x-10,y-129,26,27,27,15) and pixel_match(self.im,x+26,y-115,177,199,193,20):
            return "bajiao"
        
        '''
        mi
        ref 987 1027
        '''
        if pixel_match(self.im,x+4,y-40,232,231,219,15) and pixel_match(self.im,x+79,y-20,140,48,48,30):
            return "mi"
        '''
        daji
        ref 1166 1027
        '''
        if pixel_match(self.im,x-16,y-16,27,35,62,15) and pixel_match(self.im,x+58,y-20,27,35,62,15):
            return "daji"
        '''
        francais
        ref 1344 1027
        '''
        if pixel_match(self.im,x-17,y-45,254,241,238,15) and pixel_match(self.im,x-5,y-36,42,43,42,15):
            return "francais"
        '''
        tangshizi
        ref 1523 1027
        '''
        if pixel_match(self.im,x+68,y-16,198,207,218,15) and pixel_match(self.im,x+15,y-22,42,49,70,15):
            return "tangshizi"
        return "WILL ADD IN FUTURE"

def init_tess():
    tesser=tess()
    tesser.add_language("eng")
    tesser.set_chars("0123456789")
    tesser.set_mode("line")
    return tesser

def is_flower(im,x,y):
    return pixel_match(im,x,y,254,154,152,30)

def getdigit(x):
    new=0
    for digi in x:
        if (digi>="0") and (digi<="9"):
            new=new*10+int(digi)
    return new

def count_flower(im,startx,starty):
    count=0
    x=startx
    while x<1920 and (not pixel_match(im,x,starty,255,255,255,90)):
        if is_flower(im,x,starty):
            count+=1
            if count==1:
                startx=x
            while is_flower(im,x,starty):
                x+=1
        x+=1
    if count>0:
        return (count,startx,x)
    else:
        return (0,-1,-1)

def parse_level(im,x,y,tesser):
    im=im.crop((x-48,y-12,x-17,y+10))
    tesser.load_img(im)
    tesser.exec_tess()
    return getdigit(tesser.getresult())

def parse_player(im,tesser,flower=[],level=[],name=[],locator=[],starty=1027,echo=False):
    count=0
    intindex=len(flower)
    x=50
    while x<1800 and count<9:
        fc,x1,x2=count_flower(im,x,starty)
        if fc!=0:
            x=x2
            count+=1
            level.append(parse_level(im,x1,starty,tesser))
            flower.append(fc)
            locator.append((x1,starty))
        x+=1
    f=name_parser(im)
    for i in range(intindex,intindex+count):
        name.append(f.parse(locator[i]))
    del f
    if echo:
        return (flower,level,name,locator)

def exec_parse(im):
    flower=[]
    level=[]
    name=[]
    locator=[]
    tesser=init_tess()
    p=True
    while p==True:
        flower,level,name,locator=parse_player(im,tesser,flower,level,name,locator,echo=True)
        p=doevent.swipe_playerlist()
        im=screenshot.pull_screenshot()
    print(flower,level,name,locator)