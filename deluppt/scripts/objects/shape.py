from deluppt.scripts.functions import *
from deluppt.scripts.csys import *


''' Example
{
    "type":"shape",
    "size":[256, 256],
    "pos":[900, 900],
    "function":[
        "rrect(self.body,[0, 0, 256, 256],[255, 0, 0],radius=0.4)"
    ],
    "mask":[
        {
            "type":"function",
            "function":"rrect(surface,[0, 0, 256, 256],[255, 0, 0],radius=0.4)"
        }
    ],
    "style":[
        {
            "type": "shadow",
            "radius": 32,
            "opacity": 120
        }
    ]
}
'''

class shape:
    def __init__(self, options:dict={}, **kwargs) -> None:
        
        kwargs.update(options)
        value = kwargs.get('value', linearvalue)
        self.surface :pygame.Surface = kwargs.get('surface', None)
        self.pos = kwargs.get('pos', [0, 0])
        self.size = kwargs.get('size', [0, 0])
        self.function = kwargs.get('function', [])
        if (type(self.function) == str): self.function = [self.function]
        
        self.rect = pygame.Rect(value(self.pos)+value(self.size))
        self.body :pygame.Surface = pygame.Surface(value(self.size), pygame.SRCALPHA)

        self.render(value)
    
    def render(self, value=linearvalue) -> None:
        self.body :pygame.Surface = pygame.Surface(value(self.size), pygame.SRCALPHA)
        for function in self.function:
            try: exec(function)
            except Exception as e: out(e, WARNING)
    
    def draw(self, **kwargs) -> None:
        self.surface = kwargs.get('surface', self.surface)
        if (not self.surface): return
        
        value = kwargs.get('value', linearvalue)
        self.rect = pygame.Rect(value(self.pos)+value(self.size))
        return self.body