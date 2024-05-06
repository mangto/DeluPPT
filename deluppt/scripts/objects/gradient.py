import pygame, math
from copy import copy

from deluppt.scripts.functions import *

class gradient:
    def gradient(size, startcolor, endcolor):
        height = size[1]
        bigSurf = pygame.Surface((1,height)).convert_alpha()
        dd = 1.0/height
        if (len(startcolor) == 4): sr, sg, sb, sa = startcolor
        else: sr, sg, sb = startcolor; sa = 255
        
        if (len(endcolor) == 4): er, eg, eb, ea = endcolor
        else: er, eg, eb = endcolor; ea = 255

        rm = (er-sr)*dd
        gm = (eg-sg)*dd
        bm = (eb-sb)*dd
        am = (ea-sa)*dd
        for y in range(height):
            bigSurf.set_at((0,y),
                            (int(sr + rm*y),
                            int(sg + gm*y),
                            int(sb + bm*y),
                            int(sa + am*y))
                        )
        return pygame.transform.scale(bigSurf, size)

    def __init__(self, options:dict={}, **kwargs) -> None:
        
        kwargs.update(options)
        value = kwargs.get('value', linearvalue)
        
        self.pos = kwargs.get('pos', [0, 0])
        self.init_pos = value(copy(self.pos))
        self.size = kwargs.get('size', [0, 0])
        self.angle = kwargs.get('angle', 0)
        self.start = kwargs.get('start', [255, 255, 255])
        self.end = kwargs.get('end', [0, 0, 0])
        self.surface :pygame.Surface = kwargs.get('surface', None)
        
        self.init_angle = self.angle_step(value(self.angle))
        self.init_start = value(copy(self.start))
        self.init_end = value(copy(self.end))
        self.rect = pygame.Rect(value(self.pos) + value(self.size))
        
        self.render(value)

    def correct360(angle):
        if (angle < 0):
            while (angle <0):
                angle += 360
        
        elif (angle > 360):
            while (angle > 360):
                angle -= 360
        
        return angle
    
    def correct90(angle):
        oangle = angle
        if (angle < 0):
            while (angle <0):
                angle += 90
        
        elif (angle > 90):
            while (angle > 90):
                angle -= 90
        
        if (oangle > 90 and oangle <= 180): angle = 90-angle
        elif (oangle > 270 and oangle <= 360): angle = 90 - angle
        
        
        return angle
    
    def render(self, value):
        self.init_angle = self.angle_step(value(self.angle))
        self.body = pygame.Surface(value(self.size), pygame.SRCALPHA)
        angle = 360 - value(self.angle)
        if (value(self.angle) < 0 or value(self.angle) > 360): angle = gradient.correct360(angle)
        
        angle= self.angle_step(angle)
        
        rad = value(gradient.correct90(angle))*round(math.pi, 3)/180
        start, end = value(self.start), value(self.end)
        
        csize = (value(self.size)[0]//3, value(self.size)[1]//3)
        self.canvas = pygame.Surface(csize, pygame.SRCALPHA)
        self.gradient_surf = gradient.gradient(csize, start, end)
        self.gradient_surf = pygame.transform.rotate(self.gradient_surf, angle)
        gsize = self.gradient_surf.get_size()
        self.crossline = distance((0, 0), csize)
        

        
        seta = round(math.atan(csize[1]/csize[0]), 3)
        if (csize[0] > csize[1]): length = csize[1]/abs(round(math.sin(rad+seta), 3))
        else: length = csize[0]/abs(round(math.cos(seta-rad), 3))
        self.multiplier = (self.crossline/length)
        
        gsize = (int(gsize[0]*self.multiplier), int(gsize[1]*self.multiplier))
        self.gradient_surf = pygame.transform.smoothscale(self.gradient_surf, gsize)
        
        self.gpos = ((csize[0]-gsize[0])//2, (csize[1]-gsize[1])//2)
        self.csize = csize
        
        self.canvas.blit(self.gradient_surf, (self.gpos))
        self.body = pygame.transform.smoothscale(self.canvas, value(self.size))
        
    def angle_step(self, angle:float, step:int=2) -> float:
        
        return (angle//step)*step
    
    def draw(self, **kwargs) -> pygame.Surface:
        self.surface = kwargs.get('surface', self.surface)
        if (not self.surface): return
        
        value = kwargs.get('value', linearvalue)
        
        if ([self.angle_step(value(self.angle)),value(self.start),value(self.end)] != [self.init_angle, self.init_start, self.init_end]):
            self.render(value)
            self.uuid = uuid()
        
        if (value(self.pos) != self.init_pos):
            self.init_pos = value(self.pos)
            self.rect = pygame.Rect(list(value(self.pos)) + list(value(self.size)))
        
        return self.body