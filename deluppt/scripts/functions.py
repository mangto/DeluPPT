import pygame, os, win32api
from uuid import uuid4

def uuid() -> str:
    return str(uuid4().hex)

def linearvalue(value):
    return value

def get_all_fonts() -> list:
    return os.listdir("C:\\Windows\\Fonts")

def get_all_fontname() -> list:
    return [c[:c.rfind(".")] for c in os.listdir("C:\\Windows\\Fonts")]

fonts = { c.lower():c for c in get_all_fonts() }
fontmap = { c[:c.rfind(".")].lower():c for c in get_all_fonts() }
localfonts = { c.lower():c for c in os.listdir(".\\deluppt\\fonts")}
localfontmap = { c[:c.rfind(".")].lower():c for c in os.listdir(".\\deluppt\\fonts") }



fontmap.update(fonts)
localfontmap.update(localfonts)
    
def HitCheck(hitbox:pygame.Surface, pos:tuple[int, int]):
    try:
        if (hitbox.get_at(pos) != (0, 0, 0)): return True
        
        return False
    except:
        return False

def distance(pos1:tuple[int, int], pos2:tuple[int, int]) -> float:
    return ((pos1[0]-pos2[0])**2 + (pos1[1]-pos2[1])**2)**0.5

def check_rect_collide(rect:pygame.Rect, pos:tuple[int, int]) -> bool:
    rpos = rect.topleft
    size = rect.size
    
    collide = pos[0] >= rpos[0] and pos[0] <= rpos[0]+size[0] and pos[1] >= rpos[1] and pos[1] <= rpos[1]+size[1]
    
    return collide

lastleft1 = 0
lastleft2 = 0
lastright2 = 0
lastright1 = 0
lastmiddle1 = 0
lastmiddle2 = 0
class mouse:
    def middlebtup():
        global lastmiddle2
        middle = win32api.GetKeyState(0x04)
        if int(lastmiddle2) <0 and middle >=0:
            lastmiddle2 = middle
            return True
        else:
            lastmiddle2 = middle
            return False
    def middlebtdown():
        global lastmiddle1
        middle = win32api.GetKeyState(0x04)
        if int(lastmiddle1) >=0 and middle <0:
            lastmiddle1 = middle
            return True
        else:
            lastmiddle1 = middle
            return False
    def rightbtdown():
        global lastright1
        right = win32api.GetKeyState(0x02)
        if int(lastright1) >= 0 and right <0:
            lastright1 = right
            return True
        else:
            lastright1=right
            return False
    def rightbtup():
        global lastright2
        right = win32api.GetKeyState(0x02)
        if int(lastright2) < 0 and right >=0:
            lastright2 = right
            return True
        else:
            lastright2=right
            return False
    def leftbtdown():
        global lastleft1
        left = win32api.GetKeyState(0x01)
        if int(lastleft1) >=0 and left <0:
            lastleft1 = left
            return True
        else:
            lastleft1 = left
            return False
    def leftbtup():
        global lastleft2
        left = win32api.GetKeyState(0x01)
        if int(lastleft2) < 0 and left >= 0:
            lastleft2 = left
            return True
        
        else:
            lastleft2 = left
            return False

def rrect(surface,rect,color,radius=0.4):
    try:
        rect = pygame.Rect(rect)
        color = pygame.Color(*color)
        alpha = color.a
        color.a = 0
        pos = rect.topleft
        rect.topleft = 0,0
        rectangle = pygame.Surface(rect.size,pygame.SRCALPHA)
        circle = pygame.Surface([min(rect.size)*3]*2,pygame.SRCALPHA)
        pygame.draw.ellipse(circle,(0,0,0),circle.get_rect(),0)
        circle = pygame.transform.smoothscale(circle,[int(min(rect.size)*radius)]*2)
        radius = rectangle.blit(circle,(0,0))
        radius.bottomright = rect.bottomright
        rectangle.blit(circle,radius)
        radius.topright = rect.topright
        rectangle.blit(circle,radius)
        radius.bottomleft = rect.bottomleft
        rectangle.blit(circle,radius)

        rectangle.fill((0,0,0),rect.inflate(-radius.w,0))
        rectangle.fill((0,0,0),rect.inflate(0,-radius.h))

        rectangle.fill(color,special_flags=pygame.BLEND_RGBA_MAX)
        rectangle.fill((255,255,255,alpha),special_flags=pygame.BLEND_RGBA_MIN)
        return surface.blit(rectangle,pos)
    except: pass

def set_color(img:pygame.Surface, color:tuple[int, int, int]=(0, 0, 0)) -> pygame.Surface:
    surface = pygame.Surface(img.get_size(), pygame.SRCALPHA)
    color = pygame.Color(color[0], color[1], color[2])
    for x in range(img.get_width()):
        for y in range(img.get_height()):
            color.a = img.get_at((x, y)).a 
            surface.set_at((x, y), color)
            
    return surface

def draw_rect_alpha(surface, color, rect):
    shape_surf = pygame.Surface(pygame.Rect(rect).size, pygame.SRCALPHA)
    pygame.draw.rect(shape_surf, color, shape_surf.get_rect())
    surface.blit(shape_surf, rect)

def DrawBorder(window:pygame.Surface, rect:pygame.Rect, color:tuple, radius:int=2) -> None:
    pygame.draw.rect(window, color, rect, 1)
    pygame.draw.circle(window, color, rect.topleft, radius)
    pygame.draw.circle(window, color, rect.topright, radius)
    pygame.draw.circle(window, color, rect.bottomleft, radius)
    pygame.draw.circle(window, color, rect.bottomright, radius)

    pygame.draw.circle(window, color, (rect.centerx, rect.top), radius)
    pygame.draw.circle(window, color, (rect.left, rect.centery), radius)
    pygame.draw.circle(window, color, (rect.centerx, rect.bottom), radius)
    pygame.draw.circle(window, color, (rect.right, rect.centery), radius)
    
def font(name:str, size:int) -> pygame.font.Font:

    name = name.lower()

    try:
        if (name in localfontmap):
            return pygame.font.Font(f".\\deluppt\\fonts\\{localfontmap[name]}", size)
        
        if (name not in fontmap):
            return pygame.font.Font(f"C:\\Windows\\Fonts\\Arial.ttf", size)
        
        return pygame.font.Font(f"C:\\Windows\\Fonts\\{fontmap[name]}", size)
    except Exception as e:
        if "Couldn't find glyph" in e.args[0]:
            return
        if "Passed a Null pointer" in e.args[0]:
            return

def align_rect(text_rect, pos, cenleft) -> pygame.Rect:
    x, y = pos
    if(cenleft == "center"):
        text_rect.centerx = x
        text_rect.centery = y
        
    elif(cenleft == "left"):
        text_rect.left=x
        text_rect.top=y
        
    elif(cenleft == "right"):
        text_rect.right=x
        text_rect.top=y
    
    elif (cenleft == "btleft"):
        text_rect.left = x
        text_rect.bottom = y
        
    elif(cenleft == "btright"):
        text_rect.right=x
        text_rect.bottom=y
        
    elif(cenleft == "cenleft"):
        text_rect.left=x
        text_rect.centery=y
        
    elif(cenleft == "cenright"):
        text_rect.right=x
        text_rect.centery=y
        
    elif(cenleft == "cenbt"):
        text_rect.centerx=x
        text_rect.bottom=y
        
    elif(cenleft == "centop"):
        text_rect.centerx=x
        text_rect.top=y
    
    return text_rect

def DrawText(text, font:pygame.font.Font, window, pos, cenleft="center", color=(0,0,0)):
    text_obj = font.render(str(text), True, color)
    text_rect = text_obj.get_rect()
    
    text_rect = align_rect(text_rect, pos, cenleft)
        
    window.blit(text_obj, text_rect)

def rotate(image, angle, x, y):
    
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center = image.get_rect(center = (x, y)).center)

    return rotated_image, new_rect