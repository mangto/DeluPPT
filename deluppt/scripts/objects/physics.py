from deluppt.scripts.functions import *
from deluppt.scripts.imageloader import imageloader
from deluppt.scripts.csys import *

import math, pymunk, pymunk.pygame_util
from pymunk import Vec2d

''' Example
{
    "type":"physics",
    "size":[768, 768],
    "pos":[50, 50],
    "objects":[
        {
            "type":"segment",
            "pos1":[-100, 768],
            "pos2":[868, 768],
            "visible":0
        },
        {
            "type":"poly",
            "pos":[100, 100],
            "points":[[-32, -32], [-32, 32], [32, 32], [32, -32]],
            "image":".\\data\\axis.png"
        },
        {
            "type":"poly",
            "pos":[300, 120],
            "points":[[-32, -32], [-32, 32], [32, 32], [32, -32]],
            "image":".\\data\\axis.png"
        },
        {
            "type":"poly",
            "pos":[400, 80],
            "points":[[-32, -32], [-32, 32], [32, 32], [32, -32]],
            "image":".\\data\\axis.png"
        },
        {
            "type":"poly",
            "pos":[500, 100],
            "points":[[-32, -32], [-32, 32], [32, 32], [32, -32]],
            "image":".\\data\\axis.png"
        }
    ]
}
'''


class physics:
    def __init__(self, options:dict={}, **kwargs) -> None:
        
        kwargs.update(options)
        value = kwargs.get('value', linearvalue)
        self.surface :pygame.Surface = kwargs.get('surface', None)
        self.pos = kwargs.get('pos', [0, 0])
        self.size = kwargs.get('size', [0, 0])
        
        self.rect = pygame.Rect(value(self.pos)+value(self.size))
        self.body :pygame.Surface = pygame.Surface(value(self.size), pygame.SRCALPHA)
        
        self.objects :list[dict] = kwargs.get('objects', [])
        self.background = kwargs.get('background', None)
        self.lcolor = kwargs.get('line', (255, 0, 0))
        
        self.function = kwargs.get('function', {})
        self.counts = {}
        
        # pymunk init
        self.space = pymunk.Space()
        self.space.gravity = Vec2d(0, 981)
        self.shapes :list[pymunk.Shape] = []
        self.statics = []
        self.statics_visiblity = []
        self.polys = []
        self.imgs = []
        
        self.decode_object()
        self.render(value, 120)
    
    def flipy(self, y) -> float:
        return -y+self.size[1]
    
    def add_object(self, object:dict) -> None:
        type = object.get('type', 'dummy')
            
        if type == 'segment':
            '''
            {
                "type":"segment",
                "pos1":[x1, y1],
                "pos2":[x2, y2],
                "radius":0,
                "friction:1
            }
            '''
            a = object.get('pos1', (0, 0))
            b = object.get('pos2', (0, 0))
            r = object.get('radius', 0)
            friction = object.get('friction', 1)
            visibility = object.get('visible', 1)
            segment = pymunk.Segment(self.space.static_body, a, b, r)
            segment.friction = friction
            self.statics.append(segment)
            self.space.add(segment)
            self.statics_visiblity.append(visibility)
            pass
        elif type == 'poly':
            '''
            {
                "type":"poly",
                "points":[ [x1, y1], [x2, y2], [x3, y3], ... ],
                "mass":10,
                "pos":[x, y],
                "velocity":[0, 0]
                "friction":1,
                "angle":0,
                "image":"path"
            }
            '''
            points = object.get('points', [])
            mass = object.get('mass', 10)
            pos = object.get('pos', [0, 0])
            friction = object.get('friction', 1)
            angle = object.get('angle', 0)
            image = object.get('image', '')
            velocity = object.get('velocity', [0, 0])
            
            moment = pymunk.moment_for_poly(mass, points)
            body = pymunk.Body(mass, moment)
            shape = pymunk.Poly(body, points)
            shape.friction = friction
            body.position = pos
            body.velocity = velocity
            body.angle = angle
            
            self.space.add(body, shape)
            self.polys.append(shape)
            self.imgs.append(imageloader.load(image))
            
            pass
        else: pass
        return
    
    def decode_object(self) -> None:
        self.shapes :list[pymunk.Shape] = []
        self.statics = []
        self.polys = []
        self.imgs = []
        
        object :dict
        for object in self.objects:
            
            self.add_object(object)
            
            continue
        
        return
    
    def render(self, value, fps=120) -> None:
        # del self.body
        self.body.fill((255,255,255,0))
        if (self.background): self.body.fill(self.background)
        fps = max(fps, 50)
        
        
        dt = 1/fps/5
        for _ in range(5): self.space.step(dt)
        
        for i, poly in enumerate(self.polys):
            
            p = poly.body.position
            angle = math.degrees(poly.body.angle)
            rotated = pygame.transform.rotate(self.imgs[i], round(-angle, 1))
            offset = Vec2d(*rotated.get_size()) /2
            p = p-offset
            
            self.body.blit(rotated, (round(p.x), round(p.y)))
        
        for i, line in enumerate(self.statics):
            if (self.statics_visiblity[i]):
                body = line.body
                
                pv1 = body.position + line.a.rotated(body.angle)
                pv2 = body.position + line.b.rotated(body.angle)
                p1 = round(pv1.x), round(pv1.y)
                p2 = round(pv2.x), round(pv2.y)
                pygame.draw.lines(self.body, self.lcolor, False, [p1, p2], 2)
        
        self.rect = pygame.Rect(value(self.pos)+value(self.size))
        return
    
    def functions(self, keystate:list, events:list) -> None:
        '''
        function:{
            key:{
                "1": ...,
                "2": ...
            }
        }
        '''
        for key in self.function:
            
            if (key.startswith("mb")):
                id = key[2]
                
                exist = False
                for event in events:
                    if (event.type == pygame.MOUSEBUTTONDOWN):
                        if (str(event.button) == id): exist = True
                
                if (not exist): continue
                
            
            elif (key not in keystate[2]): continue
            
            if (key in self.counts): self.counts[key] += 1
            else: self.counts[key] = 1
            
            if ("0" in self.function[key]):
                try:
                    exec(self.function[key]["0"])
                    
                except Exception as e:
                    out(e, WARNING)
            
            count = str(self.counts[key])
            
            if (count not in self.function[key]): continue
            
            try:
                exec(self.function[key][count])
                
            except Exception as e:
                out(e, WARNING)
            
            continue
        
        return
    
    def draw(self, **kwargs) -> None:
        self.surface = kwargs.get('surface', self.surface)
        keystate = kwargs.get('keystate', [])
        events = kwargs.get('events', [])
        if (not self.surface): return
        
        value = kwargs.get('value', linearvalue)
        fps = kwargs.get('fps', 120)
        self.functions(keystate, events)
        self.render(value, fps)
        return self.body