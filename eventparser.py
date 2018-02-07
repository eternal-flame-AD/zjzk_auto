
def pixel_match(im,target_x,target_y,target_r,target_g,target_b,diff,debug=False):
    """
    try:
        im_pixel=im.load()
    except:
        return False
    pixel=im_pixel[target_x,target_y]
        old method
    """
    try:
        pixel=im.getpixel((target_x,target_y))
    except:
        print("ERROR:Out of image range")
        print("x=",target_x,' y=',target_y)
        print("image size:",im.size)
        raise RuntimeError("ERROR:Out of image range")
    if debug:
        print([target_x,target_y],pixel,[target_r,target_g,target_b])
    if abs(pixel[0]-target_r)+abs(pixel[1]-target_g)+abs(pixel[2]-target_b)<=diff:
        return True
    else:
        return False

def find_walkshop(im):
    if not in_fight(im):
        return False
    for x in range(0,1920):
        for y in range(400,800):
            if pixel_match(im,x,y,87,181,161,3):
                print(x,y)
                return True
    return False

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

def in_main(im):
    return pixel_match(im,55,66,96,84,105,6) and pixel_match(im,100,64,249,225,198,6)

def in_mode_selection(im):
    for y in range(170,220):
        if is_line(im,350,500,y,y) and is_line(im,350,500,y+3,y+3) and (not is_line(im,350,500,y+1,y+1)) and (not is_line(im,350,500,y+2,y+2)):
            return True
    return False

def in_challenge_selection(im):
    return find_line(im,50,1900,150,250,86,198,184,3,900,'x')

def find_challenge_selection_corner(im):
    return find_turningpoint(im,900,1900,800,900,86,198,184,3,900,200,-1,-1)

def find_start_button(im):
    x,y=find_challenge_selection_corner(im)
    return (x-140,y-150)

def in_player_selection(im):
    if is_line(im,620,740,362,362,182,163,114,100) and is_line(im,900,1020,362,362,182,163,114,100) and is_line(im,900,1020,362,362,182,163,114,100) and (not is_line(im,620,1020,362,362,182,163,114,15)):
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
    if pixel_match(im,1207,819,255,247,230,10):
        return 0
    if pixel_match(im,1266,926,178,175,32,10):
        return 1
    if pixel_match(im,1672,942,210,125,74,6):
        return 2
    return -1

def in_win_splash(im):
    return pixel_match(im,924,177,255,181,68,3) and pixel_match(im,888,185,255,181,68,3) and pixel_match(im,906,173,8,7,3,6)