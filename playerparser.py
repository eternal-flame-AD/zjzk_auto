from PIL import Image
from eventparser import pixel_match
from tess import tess

class name_parser:
    def __init__(self,im):
        self.im=im
    def parse(self,loc):
        x,y=loc
        print(x,y)
        '''
        baoyu:
        95 1027
        59 42 27 @100 901
        127 1013 195 57 58
        '''
        if pixel_match(self.im,x+5,y-126,59,42,27,25) and pixel_match(self.im,x+32,y-14,189,58,59,15):
            return "baoyu"
        '''
        mengxia:
        ref 273 1027
        '''
        if pixel_match(self.im,x-12,y-54,47,47,47,10) and pixel_match(self.im,x+97,y-19,27,45,63,20):
            return "mengxia"
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
    while not pixel_match(im,x,starty,255,255,255,10):
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

def parse_player(im,tesser,starty=1027,echo=False):
    flower=[]
    level=[]
    name=[]
    locator=[]
    count=0
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
    for i in range(0,count):
        name.append(f.parse(locator[i]))
    del f
    if echo:
        print ([flower,level,name,locator])


tesser=init_tess()
im=Image.open("playerparse.png",mode="r")
parse_player(im,tesser,echo=True)