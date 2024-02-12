import pygame

from deluppt.scripts.functions import *
from deluppt.scripts.csys import *


'''
"mask":[
    {
        "type":"function",
        "function":"pygame.draw.rect(...)"
    },
    {
        "type":"image",
        "path":".\\path_of_image.jpg",
        "rect":[x, y, sx, sy]
    },
    {
        "type":"text",
        "fontsize":int,
        "pos":[x, y]
        "font": "font_name",
        "align": "left",
        "text": "something",
    }
]

'''

class Mask:
    def render_mask(rect:pygame.Rect, masks:list[dict]) -> pygame.Surface:
        
        surface = pygame.Surface(rect.size, pygame.SRCALPHA)
        
        for mask in masks:
            mask_type = mask.get('type', '')
            
            if (mask_type == "function"):
                try: exec(mask.get('function', ''))
                except Exception as e: out(e, WARNING)
            elif (mask_type == "image"): continue
            elif (mask_type == "text"): continue
            
            continue
        
        return surface