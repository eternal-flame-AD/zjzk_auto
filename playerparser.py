from PIL import Image
from eventparser import pixel_match
from tess import tess

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
        print(startx)
        return (count,startx,x)
    else:
        return (0,-1,-1)

def parse_level(im,x,y,tesser):
    im=im.crop((x-48,y-12,x-17,y+10))
    tesser.load_img(im)
    tesser.exec_tess()
    return getdigit(tesser.getresult())

def parse_name(im,x,y):
    return "WILL ADD IN FUTURE"

def parse_player(im,tesser,starty=1027,echo=False):
    flower=[]
    level=[]
    name=[]
    count=0
    x=50
    while x<1800 and count<9:
        fc,x1,x2=count_flower(im,x,starty)
        if fc!=0:
            x=x2
            count+=1
            name.append(parse_name(im,x1,starty))
            level.append(parse_level(im,x1,starty,tesser))
            flower.append(fc)
        x+=1
    if echo:
        print ([flower,level,name])


tesser=init_tess()
im=Image.open("playerparse.png",mode="r")
parse_player(im,tesser,echo=True)