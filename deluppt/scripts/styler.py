import pygame
from copy import copy

from deluppt.scripts.objects.dummy import dummy
from deluppt.scripts.functions import *

def RectShadow(rect:pygame.Rect,
               radius:int,
               opacity:int,
               color:tuple[int, int, int],
               ) -> pygame.Surface:
    
    if (type(rect) != pygame.Rect): return
    if (type(radius) not in [int, float]): return
    if (type(opacity) != int): return
    if (type(color) not in [tuple, list]): return
    
    radius = int(radius)
    size = list(rect.size)
    surface = pygame.Surface((size[0]+radius*2, size[1]+radius*2), pygame.SRCALPHA)
    pygame.draw.rect(surface, color, [radius]*2+size)
    surface = pygame.transform.gaussian_blur(surface, radius)
    surface.set_alpha(opacity)
    return surface

def TextShadow(object:dummy,
               radius:int,
               opacity:int,
               color:tuple[int, int, int],
               options:dict
               ) -> pygame.Surface:
    
    if (type(radius) not in [int, float]): return
    if (type(opacity) != int): return
    if (type(color) not in [tuple, list]): return
    
    radius = int(radius)
    size = list(object.rect.size)
    surface = pygame.Surface((size[0]+radius*2, size[1]+radius*2), pygame.SRCALPHA)
    object = copy(object)
    object.color = color
    
    body = object.draw(
        value = options.get('value'),
        mouse = options.get('mouse'),
        mousestate = options.get('mousestate'),
        keystate = options.get('keystate'),
    )
    
    surface.blit(body, (radius, radius))
    surface = pygame.transform.gaussian_blur(surface, radius)
    surface.set_alpha(opacity)
    
    return surface

def MaskShadow(body:pygame.Surface,
               radius:int,
               opacity:int,
               color:tuple[int, int, int],
            ) -> pygame.Surface:
    
    if (type(radius) not in [int, float]): return
    if (type(opacity) != int): return
    if (type(color) not in [tuple, list]): return
    
    size = body.get_size()
    surface = pygame.Surface((size[0]+radius*2, size[1]+radius*2), pygame.SRCALPHA)
    mask = set_color(body, color)
    surface.blit(mask, (radius, radius))
    surface = pygame.transform.gaussian_blur(surface, radius)
    surface.set_alpha(opacity)
    
    return surface

def Blur(object:dummy, radius:int) -> pygame.Surface:
    if (type(radius) not in (float, int)): return
    
    body = object.body.copy()
    body = pygame.transform.gaussian_blur(body, radius)
    
    return body

Styles = {
    "shadow":-1,
    "original":0,
    "blur":1,
}
Prior = {
    
}


def ApplyStyle(window:pygame.Surface, object:dummy, styles:list, opacity:int=255, options:dict={}) -> pygame.Surface:
    
    uuid :str = object.uuid
    value = options.get("value", linearvalue)
    
    styles = [s for s in styles if s.get('type', '') in Styles]
    styles.append({'type':'original'})
    styles = sorted(styles, key=lambda x:Styles[x['type']])

    for style in styles:
        type = style.get('type', '')
        prior = uuid in Prior and str(type) in Prior[uuid]
        layer:pygame.Surface=None
        if (type == 'original'):
            body = object.body
            
            if (object.masked):
                mask :pygame.Surface = object.masklayer.copy()
                mask.blit(body, (0, 0), None, pygame.BLEND_ADD)
                mask.set_alpha(opacity)
                body = mask
            
            window.blit(body, value(object.pos))
        
        elif (type == "shadow"):
            radius = style.get('radius', 32)
            opacity_ = style.get('opacity', 80)
            color = style.get('color', (0, 0, 0))
            offset = style.get('offset', (0, 0))
            rect :pygame.Rect = object.rect
            
            if (prior):
                layer = Prior[uuid][str(type)]
                layer.set_alpha(opacity_*opacity/255)

                
                window.blit(layer, (rect.x-radius+offset[0], rect.y-radius+offset[1]))
                continue
            
            if (not object.masked):
                if (object.objtype == "text"): 
                    layer = TextShadow(object, radius, opacity_, color, options)
                else:
                    layer = RectShadow(rect, radius, opacity_, color)
            else:
                layer = MaskShadow(object.body, radius, opacity, color)
                
            if (not layer): continue
            layer.set_alpha(opacity_*opacity/255)
            
            window.blit(layer, (rect.x-radius+offset[0], rect.y-radius+offset[1]))
            
        
        elif (type == "blur"):
            radius = style.get('radius', 32)
            pos = value(object.pos)
            
            if (prior):
                layer = Prior[uuid][str(type)]
                layer.set_alpha(opacity)
                
                if (object.masked):
                    mask :pygame.Surface = object.masklayer.copy()
                    mask.blit(layer, (0, 0), None, pygame.BLEND_ADD)
                    mask.set_alpha(opacity)
                    layer = mask
                
                window.blit(layer, pos)
                continue
            
            layer = Blur(object, radius)
            layer.set_alpha(opacity)
            
            if (object.masked):
                mask :pygame.Surface = object.masklayer.copy()
                mask.blit(layer, (0, 0), None, pygame.BLEND_ADD)
                mask.set_alpha(opacity)
                layer = mask
            
            window.blit(layer, pos)
            
        if (uuid not in Prior): Prior[uuid] = {}
        Prior[uuid][str(type)] = layer
    
    return