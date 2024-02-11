from deluppt.scripts.imageloader import imageloader
from deluppt.scripts.functions import *

import pygame
from copy import copy

class image:
    def __init__(self, options:dict={}, **kwargs) -> None:
        
        kwargs.update(options)
        value = kwargs.get('value', linearvalue)
        
        self.pos = kwargs.get('pos', [0, 0])
        self.size = kwargs.get('size', [32, 32])
        self.path = kwargs.get('path', '')
        self.align = kwargs.get("align", "left")
        self.surface :pygame.Surface = kwargs.get('surface', None)
        
        self.org :pygame.Surface = imageloader.load(value(self.path))
        self.orgsize = self.org.get_size()
        self.rect = pygame.Rect([value(self.pos)[0], value(self.pos)[1], value(self.size)[0], value(self.size)[1]])
        
        self.img = self.org.copy()
        
        if (value(self.size) != self.orgsize):
            self.img = pygame.transform.smoothscale(self.org, value(self.size)).convert_alpha()
        self.body = self.img.copy()
        self.rect = align_rect(self.rect, value(self.pos), self.align)
        
        pass
    
    def draw(self, **kwargs) -> pygame.Surface:
        self.surface = kwargs.get('surface', self.surface)
        if (not self.surface): return
        
        value = kwargs.get('value', linearvalue)
        
        if (value(self.size) != list(self.img.get_size()) and value(self.size) != self.img.get_size()):
            self.img = pygame.transform.smoothscale(self.org, value(self.size))
            self.body = self.img
            self.uuid = uuid()
        
        self.rect = pygame.Rect([value(self.pos)[0], value(self.pos)[1], value(self.size)[0], value(self.size)[1]])
        self.rect = align_rect(self.rect, value(self.pos), self.align)

        
        
        return self.body