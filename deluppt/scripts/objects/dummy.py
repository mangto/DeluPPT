from deluppt.scripts.functions import *

class dummy:
    def __init__(self, options:dict={}, **kwargs) -> None:
        
        kwargs.update(options)
        value = kwargs.get('value', linearvalue)
        self.surface :pygame.Surface = kwargs.get('surface', None)
        self.pos = kwargs.get('pos', [0, 0])
        self.size = kwargs.get('size', [0, 0])
        
        self.rect = pygame.Rect(value(self.pos)+value(self.size))
        self.body :pygame.Surface
    
    
    def draw(self, **kwargs) -> None:
        self.surface = kwargs.get('surface', self.surface)
        if (not self.surface): return
        
        value = kwargs.get('value', linearvalue)
        return self.body