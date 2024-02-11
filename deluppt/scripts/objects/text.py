from deluppt.scripts.functions import *

import pygame
from copy import copy
import pyperclip

class text:
    
    basic_font = font('arial', 16)
    
    def __init__(self, options:dict={}, **kwargs) -> None:
        
        kwargs.update(options)
        value = kwargs.get('value', linearvalue)
        
        self.pos = kwargs.get('pos', [0, 0])
        self.init_pos = value(copy(self.pos))
        self.text :str = kwargs.get('text', '')
        self.init_text = value(copy(self.text))
        self.color :tuple = kwargs.get('color', [0, 0, 0])
        self.init_color = value(copy(self.color))
        self.fontname :pygame.font.Font = kwargs.get('font', '')
        self.init_fontname :pygame.font.Font = value(copy(self.fontname))
        self.fontsize :pygame.font.Font = kwargs.get('fontsize', 0)
        self.init_fontsize = value(copy(self.fontsize))
        self.surface :pygame.Surface = kwargs.get('surface', None)
        self.align = kwargs.get('align', 'left')
        self.FullSize = kwargs.get('FullSize', [1280, 720])
        
        self.font = font(self.fontname, int(value(self.fontsize))) if self.fontname else text.basic_font
        self.hitbox = pygame.Surface(self.FullSize)
        self.lines = str(value(self.text)).splitlines()
        
        self.heights = [0]
        self.widths = [0]
        self.points = []
        self.objects = []
        self.body:pygame.Surface
        self.rect:pygame.Rect
        self.render(value)
        self.hover = False
        self.lasthover = False
        
        self.dragstart = -1
        self.dragend = -1

        
    
    def render(self, value):
        self.init_text = value(self.text)
        self.hitbox = pygame.Surface(self.FullSize)
        self.init_fontsize = value(self.fontsize)
        self.init_fontname = self.fontname

        orgfont = self.font
        self.font = font(self.fontname, int(value(self.fontsize))) if self.fontname else text.basic_font
        try: value(self.font).size('c')
        except Exception as e: self.font = orgfont

        self.heights = [0]
        self.widths = [0]
        self.points = []
        self.objects = []
        self.lines = str(value(self.text)).splitlines()
        try:
            for line in self.lines:
                height = 0
                width = 0
                for c in line:
                    length = self.font.size(c)
                    if (length[1] > height): height = length[1]
                    
                    self.points.append((width, sum(self.heights)+height//2))
                    width += length[0]

                    
                    continue
                
                self.points.append((width, sum(self.heights)+height//2))
                
                obj = value(self.font).render(line, True, value(self.color))
                self.objects.append(obj)
                
                self.heights.append(height)
                self.widths.append(width)
                continue
            
            self.body = pygame.surface.Surface((max(self.widths), sum(self.heights)), pygame.SRCALPHA)
            self.rect = pygame.Rect([self.pos[0], self.pos[1], max(self.widths), sum(self.heights)])
            for i, obj in enumerate(self.objects):
                self.body.blit(obj, (0, sum(self.heights[:i])))
                
            pygame.draw.rect(self.hitbox, (255, 255, 255), self.rect)
        except Exception as e:
            if "Couldn't find glyph" in e.args[0]:
                return
            if "Passed a Null pointer" in e.args[0]:
                return

        pass
    
    def draw(self, **kwargs) -> pygame.Surface:
        self.surface :pygame.Surface = kwargs.get('surface', self.surface)
        if (not self.surface): return
        
        # load
        value = kwargs.get('value', linearvalue)
        if (value(self.text) != self.init_text
            or value(self.fontsize) != self.init_fontsize
            or value(self.fontname) != self.init_fontname
            or value(self.color) != self.init_color
            ):
            self.render(value)
            self.uuid = uuid()
        

            
        mouse = kwargs.get('mouse', [0, 0])
        mousestate = kwargs.get('mousestate', {})
        keystate = kwargs.get('keystate', [[], [], []])
        
        # hitbox
        self.hover = False
        if (value(self.pos) != self.init_pos):
            self.init_pos = value(self.pos)
            self.hitbox.fill((0, 0, 0))
            self.rect = pygame.Rect([self.pos[0], self.pos[1], max(self.widths), sum(self.heights)])
            self.rect = align_rect(self.rect, value(self.pos), value(self.align))
            pygame.draw.rect(self.hitbox, (255, 255, 255), self.rect)
            
        if (HitCheck(self.hitbox, mouse)): self.hover = True
        
        
        # Draw
        if (mousestate.get('leftdown')): self.dragend, self.dragstart = -1, -1
        if (self.hover):
            if (not self.lasthover): pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_IBEAM)
            
            # drag
            if (mousestate.get('leftdown')):
                self.dragstart = sorted(self.points, key=lambda x:distance([x[0]+self.rect.topleft[0], x[1]+self.rect.topleft[1]], mouse))[0]
                self.dragstart = self.points.index(self.dragstart)
                
            if (pygame.mouse.get_pressed()[0]):
                self.dragend = sorted(self.points, key=lambda x:distance([x[0]+self.rect.topleft[0], x[1]+self.rect.topleft[1]], mouse))[0]
                self.dragend = self.points.index(self.dragend)
            
        else:
            if (self.lasthover): pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        self.lasthover = self.hover
            
        if (self.dragstart != -1 and self.dragend != -1):
            points = self.points[min(self.dragstart, self.dragend) : max(self.dragstart, self.dragend)+1]
            height = max(self.heights)
            
            for i, point in enumerate(points[:-1]):
                if (point[1] != points[i+1][1]): continue
                draw_rect_alpha(self.surface, (49, 154, 185, 100), [self.rect.topleft[0]+point[0], self.rect.topleft[1]+ point[1]-height//2, points[i+1][0]-point[0], height])
            
            if ('ctrl' in keystate[0] and 'c' in keystate[0]): pyperclip.copy(str(value(self.text))[min(self.dragstart, self.dragend) : max(self.dragstart, self.dragend)])
            
            pass
        
        return self.body