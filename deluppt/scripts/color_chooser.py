import pygame, sys, json, time, copy, os
from pygame import gfxdraw
import win32api, win32con, win32gui, ctypes

pygame.init()

def texload(path:str) -> pygame.surface.Surface:
    return pygame.image.load(path)


# ==================================================
# ==================================================

def get_all_fontname() -> list:
    return [c[:c.rfind(".")] for c in os.listdir("C:\\Windows\\Fonts")]

def get_all_fonts() -> list:
    return os.listdir("C:\\Windows\\Fonts")

fonts = { c.lower():c for c in get_all_fonts() }
fontmap = { c[:c.rfind(".")].lower():c for c in get_all_fonts() }
localfonts = { c.lower():c for c in os.listdir(".\\deluppt\\fonts")}
localfontmap = { c[:c.rfind(".")].lower():c for c in os.listdir(".\\deluppt\\fonts") }



fontmap.update(fonts)
localfontmap.update(localfonts)

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
user32 = ctypes.windll.user32
FullScreen = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)

def wndProc(oldWndProc, draw_callback, hWnd, message, wParam, lParam):
    global window
    if message == win32con.WM_SIZE:
        draw_callback()
        win32gui.RedrawWindow(hWnd, None, None, win32con.RDW_INVALIDATE | win32con.RDW_ERASE)
    return win32gui.CallWindowProc(oldWndProc, hWnd, message, wParam, lParam)

lastleft1 = 0
lastleft2 = 0
lastright2 = 0
lastright1 = 0
lastmiddle1 = 0
class mouse:
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


class system:
    objects = []
    CursorChanged=False

    class ui:
        class button:
            def __init__(self, window:pygame.surface.Surface, pos:tuple[int, int], size:tuple[int, int], BgColor, radius:float=0.4,
                         text:str="", font=font("NanumSquareNeo-cBd", 10), TextColor=(0, 0, 0),
                         WindowOffset:tuple[int, int]= (0, 0),
                         OnCursor=pygame.SYSTEM_CURSOR_HAND, OrgCursor=pygame.SYSTEM_CURSOR_ARROW, OnMouseColor=(240, 240, 245),
                         function=None
                         ) -> None:
                
                system.objects.append(self)
                
                # ===================== Define =====================
                self.window = window
                self.pos = pos
                self.size = size
                self.BgColor = BgColor
                self.radius = radius

                self.text = text
                self.font = font
                self.TextColor = TextColor
                
                self.WindowOffset = WindowOffset

                self.OnCursor = OnCursor
                self.OrgCursor = OrgCursor
                self.OnMouseColor = OnMouseColor

                self.function = function
                # ==================================================


                # ====================== Calc ======================
                self.hitbox = pygame.surface.Surface(window.get_size())
                system.draw.rrect(self.hitbox, (self.pos[0], self.pos[1], self.size[0], self.size[1]), (255, 255, 255), self.radius)
                # ==================================================

                return

            def draw(self, **settings):

                # ===================== Detect =====================
                mpos = settings.get("mpos", (0, 0))
                OnCursor = self.hitbox.get_at((mpos[0]-self.WindowOffset[0], mpos[1]-self.WindowOffset[1])) != (0, 0, 0)
                # ==================================================

                color = self.BgColor
                if (OnCursor):
                    pygame.mouse.set_cursor(self.OnCursor)
                    system.CursorChanged = True
                    color = self.OnMouseColor
                    
                    if (mouse.leftbtdown() and self.function != None): self.function()
                # ====================== Draw ======================
                system.draw.rrect(self.window, (self.pos[0], self.pos[1], self.size[0], self.size[1]), color, self.radius)
                system.draw.text(self.text, self.font, self.window, int(self.pos[0]+self.size[0]/2),int(self.pos[1]+self.size[1]/2), color=self.TextColor)
                # ==================================================

                return

        class slider:

            def __init__(self, window, pos:tuple[int, int], size:tuple[int, int], title:str, radius:int=8, percentage:float=0.,
                         font=font("NanumSquareNeo-cBd", 18), TextColor=(0, 0, 0),
                         ValueFont=font("NanumSquareNeo-aLt", 12), ValueColor=(0, 0, 0), round:int=8, unit:str="", ValueMultiplier:float=1., step:int=1,
                         SliderBgColor=(132, 140, 144), SliderActiveColor=(93, 140, 217), SliderColor=(255, 255, 255),
                         SliderYOffset:int=30,
                         OnCursor=pygame.SYSTEM_CURSOR_SIZEWE, OrgCursor=pygame.SYSTEM_CURSOR_ARROW,
                         ) -> None:
                
                system.objects.append(self)

                # ===================== Define =====================
                self.window = window
                self.pos = list(pos)
                self.size = list(size)
                self.title = title
                self.radius = radius
                self.percentage = percentage
                self.moving = False

                self.font = font
                self.TextColor = TextColor
                self.ValueFont = ValueFont
                self.ValueColor = ValueColor
                self.round = round
                self.unit = unit
                self.ValueMultiplier = ValueMultiplier
                self.SliderBgColor = SliderBgColor
                self.SliderActiveColor = SliderActiveColor
                self.SliderColor = SliderColor
                self.step = step

                self.SliderYOffset = SliderYOffset

                self.OnCursor = OnCursor
                self.OrgCursor = OrgCursor
                # ==================================================


                # ====================== Calc ======================
                self.TextSize = system.draw.gettsize(title, font)
                self.SliderXPos = size[0] * percentage
                self.actual = self.percentage*self.ValueMultiplier

                self.LastOnCursor = False
                
                self.ClickedPos:tuple[int, int]
                self.clicked = False
                self.OrgSliderXPos:int
                # ==================================================

                return

            def draw(self, **settings):
                
                # =================== Detection ====================
                mpos = settings.get("mpos", (0, 0))
                SliderPos = (self.pos[0] + int(self.SliderXPos), self.pos[1]+self.TextSize[1]+self.SliderYOffset)
                distance = ((mpos[0]-SliderPos[0])**2 + (mpos[1]-SliderPos[1])**2)**0.5
                OnCursor = distance <= self.radius
                # ==================================================


                # ==================== Control =====================
                self.moving = False
                if (OnCursor):
                    pygame.mouse.set_cursor(self.OnCursor)
                    system.CursorChanged = True


                if (OnCursor and mouse.leftbtdown()):
                    self.ClickedPos = mpos
                    self.clicked = True
                    self.OrgSliderXPos = self.SliderXPos
                    pygame.mouse.set_cursor(self.OnCursor)
                    system.CursorChanged = True

                if (self.clicked):
                    self.moving = True
                    pygame.mouse.set_cursor(self.OnCursor)
                    system.CursorChanged = True

                    self.SliderXPos = min(max(0, self.OrgSliderXPos + mpos[0] - self.ClickedPos[0]), self.size[0])
                    if (mouse.leftbtup()):
                        self.clicked = False


                # ==================================================


                # ====================== Calc ======================
                window :pygame.surface.Surface = settings.get("window", self.window)
                if (self.moving):self.percentage = self.SliderXPos/self.size[0]
                self.SliderXPos = int(self.percentage*self.size[0])
                self.actual = self.percentage*self.ValueMultiplier
                self.actual = int(self.actual/self.step)*self.step
                self.percentage = self.actual/self.ValueMultiplier
                # ==================================================


                # ====================== Draw ======================
                system.draw.text(self.title, self.font, window, self.pos[0]+self.size[0]+10, self.pos[1]+self.size[1], "left", self.TextColor)
                system.draw.text(str(round(self.actual, self.round))+"  "+self.unit, self.ValueFont, window, self.pos[0]+self.size[0]+10, self.pos[1]+self.size[1]+self.TextSize[1]+5, "left", self.ValueColor)
                system.draw.rrect(window, (self.pos[0], self.pos[1]+self.TextSize[1]+self.SliderYOffset - int(self.size[1]/2), self.size[0], self.size[1]), self.SliderBgColor, 0.9)
                system.draw.rrect(window, (self.pos[0], self.pos[1]+self.TextSize[1]+self.SliderYOffset - int(self.size[1]/2), SliderPos[0]-self.pos[0], self.size[1]), self.SliderActiveColor, 0.9)
                system.draw.rrect(window, (SliderPos[0]-self.radius, SliderPos[1]-self.radius, self.radius*2, self.radius*2), self.SliderBgColor, 0.9)
                system.draw.rrect(window, (SliderPos[0]-self.radius+1, SliderPos[1]-self.radius+1, self.radius*2-2, self.radius*2-2), self.SliderColor, 0.9)
                # ==================================================

                return
            
        class value_viewer:

            def __init__(self, window, pos:tuple[int, int], title:str, value:float=0.,
                         font=font("NanumSquareNeo-cBd", 18), TextColor=(0, 0, 0),
                         ValueFont=font("NanumSquareNeo-aLt", 12), ValueColor=(0, 0, 0), round:int=8, unit:str=""
                         ) -> None:
                
                system.objects.append(self)

                # ===================== Define =====================
                self.window = window
                self.pos = pos
                self.title = title

                self.font = font
                self.TextColor = TextColor
                self.ValueFont = ValueFont
                self.ValueColor = ValueColor
                self.round = round
                self.unit = unit
                self.value = value

                # ==================================================


                # ====================== Calc ======================
                self.TextSize = system.draw.gettsize(title, font)
                # ==================================================

                return

            def draw(self, **settings):
                
                # ====================== Calc ======================
                window :pygame.surface.Surface = settings.get("window", self.window)
                # ==================================================


                # ====================== Draw ======================
                system.draw.text(self.title, self.font, window, self.pos[0], self.pos[1], "left", self.TextColor)
                system.draw.text(str(round(self.value, self.round))+"  "+self.unit, self.ValueFont, window, self.pos[0], self.pos[1]+self.TextSize[1]+5, "left", self.ValueColor)
                # ==================================================

                return

    class draw:

        def rrect(surface,rect,color,radius=0.4):
            try:
                rect         = pygame.Rect(rect)
                color        = pygame.Color(*color)
                alpha        = color.a
                color.a      = 0
                pos          = rect.topleft
                rect.topleft = 0,0
                rectangle    = pygame.Surface(rect.size,pygame.SRCALPHA)
                circle       = pygame.Surface([min(rect.size)*3]*2,pygame.SRCALPHA)
                pygame.draw.ellipse(circle,(0,0,0),circle.get_rect(),0)
                circle       = pygame.transform.smoothscale(circle,[int(min(rect.size)*radius)]*2)
                radius              = rectangle.blit(circle,(0,0))
                radius.bottomright  = rect.bottomright
                rectangle.blit(circle,radius)
                radius.topright     = rect.topright
                rectangle.blit(circle,radius)
                radius.bottomleft   = rect.bottomleft
                rectangle.blit(circle,radius)

                rectangle.fill((0,0,0),rect.inflate(-radius.w,0))
                rectangle.fill((0,0,0),rect.inflate(0,-radius.h))

                rectangle.fill(color,special_flags=pygame.BLEND_RGBA_MAX)
                rectangle.fill((255,255,255,alpha),special_flags=pygame.BLEND_RGBA_MIN)
                return surface.blit(rectangle,pos)
            except: pass
        
        def aacircle(surface, x, y, radius, color):
            gfxdraw.aacircle(surface, x, y, radius, color)
            gfxdraw.filled_circle(surface, x, y, radius, color)

        def text(text, font, window, x, y, cenleft="center", color=(0,0,0)):
            text_obj = font.render(text, True, color)
            text_rect=text_obj.get_rect()
            if(cenleft == "center"):
                text_rect.centerx = x
                text_rect.centery = y
            elif(cenleft == "left"):
                text_rect.left=x
                text_rect.top=y
            elif(cenleft == "right"):
                text_rect.right=x
                text_rect.top=y
            elif(cenleft == "cenleft"):
                text_rect.left=x
                text_rect.centery=y
            elif(cenleft == "cenright"):
                text_rect.right=x
                text_rect.centery=y
            window.blit(text_obj, text_rect)

        def gettsize(text,font):
            return font.render(text,True,(0,0,0)).get_rect().size

window = pygame.display.set_mode([512, 384], pygame.RESIZABLE)
clock = pygame.time.Clock()
pygame.display.set_caption("Color Chooser")
icon = pygame.Surface((32, 32), pygame.SRCALPHA)
pygame.display.set_icon(icon)

class System:
    timer = time.time()
    speed = 0
    pos = 800

    def event():
        system.CursorChanged = False

        for event in pygame.event.get():
            if (event.type == pygame.QUIT):
                pygame.quit()
                sys.exit()
    
    def display():
        global window
        #
        size = window.get_size()
        
        if (size[0] < 200): window = pygame.display.set_mode([200, size[1]], pygame.RESIZABLE); size = window.get_size()
        if (size[1] < 200): window = pygame.display.set_mode([size[0], 200], pygame.RESIZABLE); size = window.get_size()
        fps = clock.get_fps()
        window.fill(((40, 44, 52)))
        
        
        pygame.draw.rect(window, (Red.actual, Green.actual, Blue.actual), (30, 30, size[0]-60, max(30, size[1]-200)))
        Red.pos = 30, size[1]-150
        Red.size[0] = size[0]-125
        Green.pos = 30, size[1]-110
        Green.size[0] = size[0]-125
        Blue.pos = 30, size[1]-70
        Blue.size[0] = size[0]-125
        
        # ==================================================
        for object in system.objects: object.draw(
                mpos=pygame.mouse.get_pos()
        )

        # ==================================================

        if (not system.CursorChanged): pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        
        pygame.display.update()
        
hwnd = pygame.display.get_wm_info()['window']
oldWndProc = win32gui.SetWindowLong(hwnd, win32con.GWL_WNDPROC, lambda *args: wndProc(oldWndProc, System.display, *args))

Red = system.ui.slider(window, (28 , 80), (255, 2), "Red", unit="", ValueMultiplier=255,
                                  TextColor=(255, 0, 0), ValueColor=(201, 201, 201), SliderActiveColor=(255, 0, 0),
                                  SliderYOffset=0)
Green = system.ui.slider(window, (28, 80 + 40*1), (255, 2), "Green", unit="", ValueMultiplier=255,
                                   TextColor=(0, 255, 0), ValueColor=(201, 201, 201), SliderActiveColor=(0, 255, 0),
                                  SliderYOffset=0)
Blue = system.ui.slider(window, (28, 80 + 40*2 ), (255, 2), "Blue", unit="", ValueMultiplier=255,
                                  TextColor=(0, 0, 255), ValueColor=(201, 201, 201), SliderActiveColor=(0, 0, 255),
                                  SliderYOffset=0)



while __name__ == "__main__":
    System.event()
    System.display()
    clock.tick(120)