import pygame
from pathlib import Path
from os.path import isfile
from json import load, dump
import ctypes, time, math
from copy import copy, deepcopy

from deluppt.scripts.imageloader import imageloader
from deluppt.scripts.objects import *
from deluppt.scripts.functions import *
from deluppt.scripts.animator import animator
from deluppt.scripts.styler import ApplyStyle
from deluppt.scripts.keyboard import *
from deluppt.scripts.transition import *
from deluppt.scripts.csys import *

pygame.init()

path = Path(__file__).parent.absolute()
deluppt_path = path.parent
user32 = ctypes.windll.user32
FullSize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)


class window:
    
    size = (1280, 720)
    mouse = (0, 0)
    basic_icon = imageloader.load( str(deluppt_path) + '\\data\\CREAM.png' , convert=False)
    MouseState = {"leftup":0, "leftdown":0, "middleup":0, "middledown":0, "rightup":0, "rightdown":0}
    KeyboardState = [[], [], []]
    
    def __init__(self,
                 size:tuple=(1280, 720),
                 caption:str="Delu PPT",
                 flags:int=pygame.RESIZABLE|pygame.DOUBLEBUF,
                 icon:pygame.Surface=None,
                 background:tuple[int, int, int]= (255, 255, 255),
                 ) -> None:
        global FullSize
        
        self.init = False
        self.size = size
        self.csize = size
        self.caption = caption
        self.flags = flags
        self.icon = icon if icon else window.basic_icon
        self.background = background
        
        self.window = pygame.display.set_mode(size, flags)
        self.canvas = pygame.surface.Surface(FullSize, pygame.SRCALPHA)
        self.cpos = (0, 0)
        self.maxsize = FullSize
        pygame.display.set_caption(self.caption, self.caption)
        pygame.display.set_icon(self.icon)
        
        self.hwnd = pygame.display.get_wm_info()['window']
        self.clock = pygame.time.Clock()
        
        
        self.index = 0
        self.pages = []
        self.aotobj:dict = None
        self.aot = {}
        self.current :dict = None
        self.full = False
        self.oldsize = self.size
        self.start:time.time = time.time()
        self.last_save = time.time()
        self.last_reload = time.time()
        self.click = 0
        
        self.movingobj = False
        self.movingstpos = (0, 0)
        self.movingobjindex = 0
        
        self.transition_start = time.time()
        self.transition = 0
        
        self.transition_objects = []
        
        self.data = {}
        pass
    
    def move_page(self, index:int) -> None:
        if (type(index) != int): return
        if (not (0 <= index and index < len(self.pages))): return
        self.click = 0
        self.start = time.time()
        self.transition_start = time.time()
        if (type(self.index) == tuple): self.index = self.index[1]
        self.transition = self.current[self.index].get('transition', 0)
        if (self.transition > 0): self.index = (self.index, index)
        else: self.index = index
        
        self.transition_objects = transition.sort_similar_objects(self.current[self.index[0]]["objects"], self.current[self.index[1]]["objects"])
        
    def decode_objects(self, objects:list) -> list:
        self.window.fill(self.background)
        color = max([[0, 0, 0], [255, 255, 255]], key=lambda x:distance(x, list(self.background)))
        size = self.window.get_size()
        DrawText("LOADING", text.basic_font, self.window, (size[0]//2, size[1]//2), "center", color)
        pygame.display.update()
        result = []
        tags = []
        for object in objects:
            
            obj_type = object.get('type', '')
            
            match obj_type:
                case "image": method = image
                case "text": method = text
                case "blur": method = blur
                case "gradient": method = gradient
                case _: continue

            obj = method(options = object, value = self.value, FullSize=self.maxsize)
            obj.animation = object.get("animation", [])
            obj.styles = object.get("style", [])
            obj.tag = object.get("tag", '')
            obj.uuid = uuid()
            obj.objtype = obj_type
            
            if (obj.tag):
                if (obj.tag in tags):
                    out(f"Warning: Same Tags Exist ({obj.tag})", WARNING, True)
                    out(f'  > "{obj.tag}" Tag Would Be Applied To {obj}', OKCYAN)
                else: tags.append(obj.tag)
            
            result.append(
                obj
                )
            
            obj.draw(
                surface=self.canvas,
                value=self.value,
                mouse=window.mouse,
                mousestate=window.MouseState,
                keystate=window.KeyboardState,
            ) # pre render -> move pages faster
            
            ApplyStyle(
                self.canvas,
                obj,
                obj.styles,
                255,
                options={
                    "value":self.value,
                    "mouse":window.mouse,
                    "mousestate":window.MouseState,
                    "keystate":window.KeyboardState,
                }
            ) # pre render -> move pages faster
            
        return result
    
    def decode_page(self, page:dict) -> dict:
        
        page = deepcopy(page)
        objects = page.get('objects', [])
        
        page['objects'] = self.decode_objects(objects)
        
        return page
        
    def reload(self) -> None:
        global FullSize
        self.index = 0
        self.click = 0
        self.start = time.time()
        if( not self.init):self.window = pygame.display.set_mode(self.size, self.flags); self.init=True
        self.canvas = pygame.surface.Surface(self.maxsize, pygame.SRCALPHA)
        pygame.display.set_caption(self.caption, self.caption)
        pygame.display.set_icon(self.icon)
        
        
        if (len(self.pages) >= self.index):
            self.current = [self.decode_page(page) for page in self.pages]
        self.aot = self.decode_objects(self.aotobj)
        return
    
    def unpack(self, data:dict) -> bool:
        self.data = deepcopy(data)
        # try:
        if True:
            self.caption = data.get('title', self.caption)
            self.size = data.get('size', self.size)
            self.flags = data.get('flags', self.flags)
            self.background = data.get('background', self.background)
            self.pages = data.get('pages', self.pages)
            self.maxsize = data.get('maxsize', FullSize)
            self.aotobj = data.get('AOT', [])
            self.save_time = data.get("save", -1)
            self.last_save = time.time()
            self.reload_time = data.get("reload", -1)
            self.last_reload = time.time()
            self.reload()
        
            return True
        
        # except Exception as e:
            print("Exception Occured While Unpacking: ", e)
            
            return False
    
    def load(self, ppt:str|dict) -> bool:        
        self.ppt = ppt
        if (type(ppt) == dict):
            return self.unpack(ppt)
        
        if (not isfile(ppt)): return False
        
        with open(ppt, "r", encoding="utf8") as file:
            data = load(file)
        
        # unpack
        return self.unpack(data)
    
    def fullscreen(self) -> None:
        if (not self.full):
            self.oldsize = self.size
            self.window = pygame.display.set_mode(FullSize, pygame.FULLSCREEN | self.flags)
            self.size = FullSize
            
        else:
            self.window = pygame.display.set_mode(self.oldsize, self.flags)
            self.size = self.oldsize
            
        self.full = self.full == 0
        
        return
    
    def value(self, value):
        if (type(value) != str): return value
        
        if (value.isnumeric()): return int(value)
        
        window = self
        token = value.split(' ')
        if (token[0] == 'match'): return self.offset_destination(self.value(value[6:]))
        if (token[0] == 'dynamic'): return eval(value[8:])
        if (token[0] == 'image'): return imageloader.load(value[6:])
        if (token[0] == 'font'): return font(token[1], self.value(token[2]))
        if (token[0] == 'relative'):
            # relative 32 1920 window.size[0] True
            if (not type(token[1].isnumeric()) and not type(token[2].isnumeric())): return 0
            val = int(token[1])/int(token[2])*eval(token[3])
            if (len(token) >= 4 and eval(token[4])): val = int(val)
            
            return val
        
        return value
        
    def offset_destination(self, pos:tuple[int, int]) -> tuple[int, int]:
        return max(int((pos[0]-self.cpos[0])/self.csize[0]*self.maxsize[0]), 0), max(int((pos[1]-self.cpos[1])/self.csize[1]*self.maxsize[1]), 0)
    
    def move_object(self):
        if (type(self.index) == tuple): return
        if (not self.current): return
        objects = self.current[self.index].get('objects', [])
        pageobj = self.pages[self.index].get('objects', [])
        if (window.MouseState['middledown']):
            for i, object in enumerate(reversed(objects)):
                obj :dict = pageobj[len(objects) - i - 1]
                moveable = obj.get('moveable', 1)
                
                if (not moveable): continue
                rect : pygame.Rect
                try: rect :pygame.Rect = object.rect
                except: continue
                
                if (not check_rect_collide(rect, window.mouse)): continue
                clickpos = window.mouse
                self.movingobj = object
                self.movingstpos = clickpos
                self.movingobjindex = i
                return
        
        if (self.movingobj):
            self.movingobj.pos = [self.movingobj.pos[0] + self.mouse[0]-self.movingstpos[0],
                              self.movingobj.pos[1] + self.mouse[1]-self.movingstpos[1]]
            self.movingstpos = self.mouse
            self.pages[self.index]['objects'][len(objects) - self.movingobjindex-1]['pos'] = self.movingobj.pos
            
        if (window.MouseState['middleup']):
            self.movingobj = False
            
        return
    
    def save(self):
        if (type(self.ppt) != str): return
        if (not isfile(self.ppt)): return
        
        self.last_save = time.time()
        with open(self.ppt, 'r', encoding='utf8') as file:
            ppt = load(file)    
            
        with open(self.ppt, 'w', encoding='utf8') as file:
            ppt['pages'] = self.pages
            dump(ppt, file, indent='\t', ensure_ascii=False,)
        
        return
    
    def render_object(self, object, opacity) -> None:
        opacity = opacity if (opacity != None) else 255
        # animator
        animations = object.animation
        t = time.time()
        for animation in animations:
            value = animator.decode(t-self.start, object, self, animation,)
            target :str = animation.get("target", None)
            
            if (value == None or target == None): continue
            try:
                if (type(value) == str): exec(target.replace("self", "object") + " = '" + str(value) +"'")
                else: exec(target.replace("self", "object") + " = " + str(value))
            except Exception as e:
                print(e)
        
        # style & draw
        
        body :pygame.Surface = object.draw(
            surface=self.canvas,
            value=self.value,
            mouse=window.mouse,
            mousestate=window.MouseState,
            keystate=window.KeyboardState,
        )
        body.set_alpha(opacity)
        
        if (object.styles):
            styles = animations = object.styles
            ApplyStyle(
                self.canvas,
                object,
                styles,
                opacity,
                options={
                    "value":self.value,
                    "mouse":window.mouse,
                    "mousestate":window.MouseState,
                    "keystate":window.KeyboardState,
                }
                )
        else:
            self.canvas.blit(body, self.value(object.pos))
        
        # border
        if ('alt' in window.KeyboardState[0]):
            try:
                rect :pygame.Rect = object.rect
                DrawBorder(self.canvas, rect, (255, 0, 0), 3)
                
            except:
                pass
    
    def render(self) -> None:
        if (not self.current): return
        
        if (type(self.index) == int):
            background = self.current[self.index].get('background', self.background)
            objects = self.current[self.index].get('objects', [])
            opacity = self.current[self.index].get('opacity', 255)
            self.canvas.fill(background)
            
            for i, object in enumerate(objects + self.aot):
                if (i == len(objects)): opacity=255
                self.render_object(object, opacity)
            
            multiplier = min(self.size[0]/self.maxsize[0], self.size[1]/self.maxsize[1])
            if (round(multiplier, 1) == 1.0): self.window.blit(self.canvas, (0, 0)); self.csize = FullSize
            else:
                target_size = int(self.maxsize[0]*multiplier), int(self.maxsize[1]*multiplier)
                pos = (self.size[0]-target_size[0])//2, (self.size[1]-target_size[1])//2
                self.cpos = pos
                self.csize = target_size
                canvas = pygame.transform.smoothscale(self.canvas, target_size)
                self.window.blit(canvas, pos)
            
            return
        
        else: # while transition
            # transiton: pos, size, (text)
            self.start = time.time()
            background = self.current[self.index[1]].get('background', self.background)
            objects = self.transition_objects
            opacity1 = self.current[self.index[0]].get('opacity', 255)
            opacity2 = self.current[self.index[1]].get('opacity', 255)
            self.canvas.fill(background)
            
            t = self.start
            estimated = (t-self.transition_start)/(self.transition+0.1**32) # float between 0 and 1
            a = round(opacity1 * (-1*(estimated-1)**2+1))
            b = round(opacity2 * (-1*estimated**2+1))
            
            for i, object in enumerate(list(objects.keys()) + self.aot):
                if (type(object) == tuple):
                    obj2 = copy(object[0])
                    obj1 = copy(object[1])
                    try:
                        s1 = animator.get_current(t-self.transition_start, 0, self.transition, object[0].size, object[1].size, self.value, True)
                        s2 = animator.get_current(t-self.transition_start, 0, self.transition, object[0].size, object[1].size, self.value, True)
                        if (s1): obj1.size = s1
                        if (s2): obj2.size = s2
                    except AttributeError: pass
                    
                    try:
                        p1 = animator.get_current(t-self.transition_start, 0, self.transition, object[0].pos, object[1].pos, self.value, True)
                        p2 = animator.get_current(t-self.transition_start, 0, self.transition, object[0].pos, object[1].pos, self.value, True)
                        if (p1): obj1.pos = p1
                        if (p2): obj2.pos = p2
                    except AttributeError: pass
                    
                    self.render_object(obj1, a)
                    self.render_object(obj2, b)
                    
                    del obj1, obj2
                    
                else:
                    if (object in objects):
                        id = objects[object]
                        if (id): opacity = a
                        else: opacity = b
                    else: opacity = 255
                    self.render_object(object, opacity)
            
            multiplier = min(self.size[0]/self.maxsize[0], self.size[1]/self.maxsize[1])
            if (round(multiplier, 1) == 1.0): self.window.blit(self.canvas, (0, 0)); self.csize = FullSize
            else:
                target_size = int(self.maxsize[0]*multiplier), int(self.maxsize[1]*multiplier)
                pos = (self.size[0]-target_size[0])//2, (self.size[1]-target_size[1])//2
                self.cpos = pos
                self.csize = target_size
                canvas = pygame.transform.smoothscale(self.canvas, target_size)
                self.window.blit(canvas, pos)
            
            if (time.time() - self.transition_start >= self.transition): self.index = self.index[1]
            
            return
    
    def update(self, **kwargs) -> None:
        window.mouse = self.offset_destination(pygame.mouse.get_pos())
        self.size = self.window.get_size()
        window.MouseState = {"leftup":mouse.leftbtup(), "leftdown":mouse.leftbtdown(),
                             "middleup":mouse.middlebtup(), "middledown":mouse.middlebtdown(),
                             "rightup":mouse.rightbtup(), "rightdown":mouse.rightbtdown()}
        if (pygame.mouse.get_focused()):
            window.KeyboardState = keyboard.get_input()
        else: window.KeyboardState = [[], [], []]
        
        self.move_object()
        
        
        if ('ctrl' in window.KeyboardState[0] and 's' in window.KeyboardState[0]): self.save()
        try:
            if (self.reload_time > 0 and time.time() - self.last_reload >= self.reload_time ):
                with open(self.ppt, "r", encoding="utf8") as file:
                    data = load(file)
                    
                if (data != self.data):
                    st = self.start
                    self.load(self.ppt)
                    self.start = st
        except: pass
        # update
        
        self.window.fill(self.background)
        self.render()
        pygame.display.update()
        self.clock.tick(300)
        return None