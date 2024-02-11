import pygame
from os.path import isfile
from copy import copy

pygame.init()

class imageloader:

    extensions = ['png', 'jpg', 'jpeg', 'gif', 'bmp', 'jfif']
    loaded = {} # path:Surface
    
    def load(path:str, convert:bool=True) -> pygame.Surface:
        if (type(path) != str or not isfile(path)):
            print("Invalid Path or File Doesn't Exists: ", path)
            return pygame.Surface((64, 64))
        
        extension = path[path.rfind(".")+1:]
        if (extension.lower() not in imageloader.extensions):
            print("Invalid File Extension: ", extension)
            return pygame.Surface((64, 64))
        
        # real load
        
        if (path in imageloader.loaded): return copy(imageloader.loaded[path])
        
        img = pygame.image.load(path)
        if (convert): img = img.convert_alpha()
        imageloader.loaded[path] = copy(img)
        
        return img