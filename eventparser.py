from tess import tess

def tess_init():
    global tesser
    try:
        tesser=tess()
        tesser.set_mode("line")
        tesser.set_chars("0123456789/")
        tesser.add_language("zjzk_level")
        return True
    except:
        return False

def to_black_and_white(im):
    w,h=im.size
    for x in range(0,w):
        for y in range(0,h):
            if pixel_match(im,x,y,255,255,255,320) and is_grey(im,x,y,10):
                im.putpixel((x,y),(255,255,255,255))
            else:
                im.putpixel((x,y),(0,0,0,0))
    return im

def seven_error_postprocess(s):
    res=""
    for pos in range(0,len(s)-1):
        if (s[pos:pos+1]==" 7") or (s[pos:pos+1]=="7 "):
            res+='/'
        else:
            res=s[pos]
    return res

def exp_refine(s):
    try:
        s.index("/")
    except ValueError:
        s=seven_error_postprocess(s)
    pos=0
    maxpos=len(s)-1
    try:
        while not (s[pos]>='0' and s[pos]<='9'):
            pos+=1
        start1=pos
        while (s[pos]>='0' and s[pos]<='9'):
            pos+=1
        exp1=int(s[start1:pos])
        while not (s[pos]>='0' and s[pos]<='9'):
            pos+=1        
        start2=pos
        while pos!=maxpos+1 and (s[pos]>='0' and s[pos]<='9'):
            pos+=1
        exp2=int(s[start2:pos])
        return exp1,exp2
    except:
        return ('failed to parse... Raw result:'+s)

def parse_player_level(im,xmin,xmax,yref=738,ymin=728,ymax=748):
    global tesser
    lastx=0
    for x in range(xmin,xmax):
        if pixel_match(im,x,yref,255,255,255,150):
            lastx=x
    lastx+=10
    im1=im.crop((xmin,ymin,lastx,ymax))
    im1=to_black_and_white(im1)
    tesser.load_img(im1)
    tesser.exec_tess()
    return exp_refine(tesser.getresult())

def parse_winner_location(im,xmin,xmax,yref=750):
    for x in range(xmin,xmax):
        if pixel_match(im,x,yref,160,115,42,50) and pixel_match(im,x+12,yref,15,10,6,30):
            return x-2

def parse_level(im):
    pos1=parse_winner_location(im,380,750)
    pos2=parse_winner_location(im,pos1+233,1000)
    pos3=parse_winner_location(im,pos2+233,1600)
    try:
        return parse_player_level(im,pos1,pos1+180),parse_player_level(im,pos2,pos2+180),parse_player_level(im,pos3,pos3+180)
    except:
        return -1
    
def is_grey(im,x,y,diff):
    pixel=im.getpixel((x,y))
    r=pixel[0]
    g=pixel[1]
    b=pixel[2]
    if abs(r-g)+abs(g-b)+abs(b-r)<=diff:
        return True
    return False

def pixel_match(im,target_x,target_y,target_r,target_g,target_b,diff,debug=False):
    """
    try:
        im_pixel=im.load()
    except:
        return False
    pixel=im_pixel[target_x,target_y]
        old method
    """
    pixel=im.getpixel((target_x,target_y))
    if debug:
        print([target_x,target_y],pixel,[target_r,target_g,target_b])
    if abs(pixel[0]-target_r)+abs(pixel[1]-target_g)+abs(pixel[2]-target_b)<=diff:
        return True
    else:
        return False

def find_walkshop(im):
    return pixel_match(im,1617,865,251,236,207,50)

def is_line(im,x1,x2,y1,y2,r=0,g=0,b=0,diff=0):
    if x1>x2:
        x1=x1+x2
        x2=x1-x2
        x1=x1-x2
    if y1>y2:
        y1=y1+y2
        y2=y1-y2
        y1=y1-y2
    for x in range(x1,x2+1):
        for y in range(y1,y2+1):
            if not pixel_match(im,x,y,r,g,b,diff):
                return False
    return True

def find_line(im,x1,x2,y1,y2,r=0,g=0,b=0,diff=0,minlength=0,direction='x'):
    if direction=='x':
        for y in range(y1,y2):
            for x in range(x1,x2-minlength):
                if is_line(im,x,x+minlength,y,y,r,g,b,diff):
                    return True
    else:
        for x in range(x1,x2):
            for y in range(y1,y2-minlength):
                if is_line(im,x,x,y,y+minlength,r,g,b,diff):
                    return True
    return False

def find_turningpoint(im,x1,x2,y1,y2,r,g,b,diff,minx,miny,xdelta=-1,ydelta=-1):
    for x in range(x1,x2+1):
        for y in range(y1,y2+1):
            if is_line(im,x,x,y,y+(ydelta*miny),r,g,b,diff) and is_line(im,x,x+(xdelta*minx),y,y,r,g,b,diff):
                return (x,y)
    raise RuntimeError("No start button found!")

def in_fight(im):
    return (not is_line(im,41,68,41,70,188,163,88,80)) and is_line(im,41,48,41,70,188,163,88,80) and is_line(im,61,68,41,70,188,163,88,80)

def max_full_count(s):
    count=0
    for level in s:
        try:
            if level[0]==0 and level[1]==0:
                count+=1
        except:
            pass
    return count

def in_benzhen(im):
    return pixel_match(im,668,65,174,54,37,20) and pixel_match(im,672,43,209,148,20,20) and pixel_match(im,668,51,11,0,0,10)

def in_main(im):
    return pixel_match(im,55,66,96,84,105,6) and pixel_match(im,100,64,249,225,198,6)

def in_mode_selection(im):
    for y in range(170,220):
        if is_line(im,100,260,y,y,diff=10) and is_line(im,480,660,y+3,y+3,diff=10) and is_line(im,100,260,y+1,y+1,160,126,88,90) and (not is_line(im,480,660,y+2,y+2)):
            return True
    return False

def in_challenge_selection(im):
    return find_line(im,50,1900,150,250,86,198,184,3,900,'x')

def find_challenge_selection_corner(im):
    return find_turningpoint(im,900,1900,180,280,86,198,184,3,900,200,-1,1)

def find_start_button(im):
    x,y=find_challenge_selection_corner(im)
    return (x-200,y+469)

def in_player_selection(im):
    if is_line(im,10,580,240,270,38,30,27,15) and is_line(im,5,500,300,305,210,210,210,100):
        return True
    return False

def in_loading_screen(im):
    return is_line(im,1,1900,20,20,0,0,0,0)

def win_presplash_ready(im):
    return pixel_match(im,948,1018,255,255,255,3)

def in_win_presplash(im):
    return pixel_match(im,797,273,255,120,120,10) and pixel_match(im,1121,285,253,97,97,10)

def determine_win_type(im):
    """
        called after in_win_splash
        0-normal
        1-something happened
        2-after something happened
    """
    if pixel_match(im,1420,925,137,137,29,10):
        return 1
    if pixel_match(im,1133,923,241,207,139,10):
        return 0
    if pixel_match(im,1420,925,64,50,33,10) and pixel_match(im,1691,998,183,108,44,30):
        return 2
    return -1

def in_win_splash(im):
    return pixel_match(im,923,133,255,181,68,6) and pixel_match(im,906,173,11,9,4,6)