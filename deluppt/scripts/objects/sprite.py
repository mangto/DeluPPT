from deluppt.scripts.imageloader import imageloader
from deluppt.scripts.functions import *

import pygame, time
from copy import copy

class sprite:
    def __init__(self, options:dict={}, **kwargs) -> None:
        
        kwargs.update(options)
        value = kwargs.get('value', linearvalue)
        
        self.pos = kwargs.get('pos', [0, 0])
        self.size = kwargs.get('size', [32, 32])
        self.path = kwargs.get('path', [])
        self.duration = kwargs.get('duration', 0.5)
        if (type(self.path) == str): self.path = [self.path]
        self.align = kwargs.get("align", "left")
        self.surface :pygame.Surface = kwargs.get('surface', None)
        self.rect = pygame.Rect([value(self.pos)[0], value(self.pos)[1], value(self.size)[0], value(self.size)[1]])
        self.last_transition = kwargs.get('local_time', time.time())
        
        self.orgs = [] # originals
        self.sizes = []
        self.imgs = []
        self.index = 0
        self.body :pygame.Surface
        
        self.reload(value)
        
        # self.org :pygame.Surface = [imageloader.load(value(path)) for path in self.path]
        # self.orgsize = self.org[0].get_size()
        
        # self.imgs = self.org.copy()
        
        # if (value(self.size) != self.orgsize):
        #     self.imgs = pygame.transform.smoothscale(self.org, value(self.size)).convert_alpha()
        # self.body = self.img.copy()
        # self.rect = align_rect(self.rect, value(self.pos), self.align)
        
        pass
    
    def reload(self, value) -> None:
        
        self.last_transition = time.time() - value(self.duration)
        self.orgs = [] # originals
        self.sizes = []
        self.imgs = []
        
        for path in self.path:
            image :pygame.Surface = imageloader.load(value(path))
            size = image.get_size()
            
            self.orgs.append(image)
            self.sizes.append(size)
            image = image.copy()
            if (size != value(self.size)): image = pygame.transform.smoothscale(image, value(self.size))
            self.imgs.append(image)
            self.uuid = uuid()
            
            continue
        
        return
    
    def draw(self, **kwargs) -> pygame.Surface:
        self.surface = kwargs.get('surface', self.surface)
        if (not self.surface): return
        
        value = kwargs.get('value', linearvalue)
        
        if (value(self.size) != list(self.imgs[self.index].get_size()) and value(self.size) != self.imgs[self.index].get_size()):
            self.reload(value)
        
        t = copy(kwargs.get('local_time', time.time()))
        if (t - self.last_transition >= value(self.duration)):
            self.last_transition = t
            self.index += 1
            if (self.index >= len(self.imgs)): self.index = 0
            self.body = self.imgs[self.index]
        
        self.rect = pygame.Rect([value(self.pos)[0], value(self.pos)[1], value(self.size)[0], value(self.size)[1]])
        self.rect = align_rect(self.rect, value(self.pos), self.align)
        
        
        return self.imgs[self.index]