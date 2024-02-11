from deluppt.scripts.functions import *
import time
import numpy as np


class blur:
    def __init__(self, options:dict={}, **kwargs) -> None:
        
        kwargs.update(options)
        value = kwargs.get('value', linearvalue)
        
        self.pos = kwargs.get('pos', [0, 0])
        self.size = kwargs.get('size', [0, 0])
        self.radius = kwargs.get('radius', 5)
        self.surface :pygame.Surface = kwargs.get('surface', None)
        self.canvas = pygame.Surface([value(self.size)[0]+value(self.radius), value(self.size)[1]+value(self.radius)])
        self.body = pygame.Surface(value(self.size))
        self.noise = kwargs.get("noise", "")
        if (self.noise):
            self.noisesurface = pygame.Surface(value(self.size))
            token = self.noise.split(' ')
            self.noisesurface = blur.add_noise(self.noisesurface, eval(token[0]), eval(token[1]))
        
        self.rect = pygame.Rect(list(value(self.pos)) + list(value(self.size)))
    
    def add_noise(surface, scale, intensity):
        noise_small = np.random.random(surface.get_size()) * intensity + (1 - intensity) / 2
        noise_big = np.repeat(np.repeat(noise_small, scale, axis=0), scale, axis=1)
        noise_big = np.uint8(noise_big * 255)
        noise_big = np.dstack([noise_big] * 3)
        noise_big = pygame.surfarray.make_surface(noise_big)
        surface.blit(noise_big, (0, 0), None, pygame.BLEND_RGB_MULT)
        
        return surface
    
    def draw(self, **kwargs) -> pygame.Surface:
        self.surface :pygame.Surface = kwargs.get('surface', self.surface)
        if (not self.surface): return
        
        # load
        value = kwargs.get('value', linearvalue)
        radius = value(self.radius)
        pos = value(self.pos)
        
        # calculate
        self.canvas.blit(self.surface, (-1*pos[0]+radius//2, -1*pos[1]+radius//2))
        self.canvas = pygame.transform.gaussian_blur(self.canvas, self.radius)
        if (self.noise): self.canvas.blit(self.noisesurface, (0, 0), None, pygame.BLEND_RGB_ADD)
        self.body.blit(self.canvas, (-1*radius//2, -1*radius//2))
        self.rect = pygame.Rect(list(value(self.pos)) + list(value(self.size)))
        
        # draw
        
        
        return self.body