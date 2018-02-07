
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
    if not in_fight(im):
        return False
    for x in range(0,1920):
        for y in range(400,800):
            try:
                pixel_match(im,x,y,87,181,161,3)
            except:
                print(x,y)
            if pixel_match(im,x,y,87,181,161,3):
                return True
    return False

def is_line(im,x1,x2,y1,y2,r=0,g=0,b=0,diff=0):
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
    return (0,0)

def in_fight(im):
    return False

def in_main(im):
    return pixel_match(im,55,66,96,84,105,6) and pixel_match(im,100,64,249,225,198,6)

def in_war_selection(im):
    for y in range(170,220):
        if is_line(im,350,500,y,y) and is_line(im,350,500,y+3,y+3) and (not is_line(im,350,500,y+1,y+1)) and (not is_line(im,350,500,y+2,y+2)):
            return True
    return False

def in_challenge_selection(im):
    return find_line(im,50,1900,150,250,86,198,184,3,900,'x')

def find_challenge_selection_corner(im):
    return find_turningpoint(im,50,1900,800,900,86,198,184,3,900,200,-1,-1)

def find_start_button(im):
    x,y=find_challenge_selection_corner(im)
    return (x-140,y-150)

def in_player_selection(im):
    return False