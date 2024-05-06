from deluppt.scripts.functions import *
from math import *

'''
{
    "type":"graph",
    "pos":[256, 256],
    "interval":30
    "range":[ [-5, 5], [-5, 5] ] # xrange, yrange,
    "showaxis":1,
    "axiscolor":[255, 255, 255],
    "axiswidth":3
    "function":[
        {
            "type":"equation",
            "equation":"y=sin(x)",
            "color":[255, 0, 0]
        },
        {
            "type":"points",
            "points":[],
            "color":[0, 255, 0]
        },
        {
            "type":"points",
            "points":"[(cos(t), sin(t)) for t in range(100)]",
            "color":[0, 255, 0]
        }
    ]
}
'''


class graph:
    def __init__(self, options:dict={}, **kwargs) -> None:
        
        kwargs.update(options)
        value = kwargs.get('value', linearvalue)
        self.value = value
        self.surface :pygame.Surface = kwargs.get('surface', None)
        self.pos = kwargs.get('pos', [0, 0])
        self.size = kwargs.get('size', [0, 0])
        self.interval = kwargs.get('interval', [30, 30])
        self.range = kwargs.get('range', [[-5, 5], [-5, 5]])
        self.function = kwargs.get('function', [])

        self.showaxis = kwargs.get('showaxis', 1)
        self.axiscolor = kwargs.get('axiscolor', [255, 255, 255])
        self.axiswidth = kwargs.get('axiswidth', 3)

        self.renderstep = kwargs.get('renderstep', 5)
        
        self.rect = pygame.Rect(value(self.pos)+value(self.size))
        self.body :pygame.Surface

        self.render(value = value)
    
    def calcpos(self, pos:list[int, int]) -> list[int, int]:
        range = self.value(self.range)
        interval = self.value(self.interval)
        lefttop = min(range[0]), max(range[1])
        dx, dy = pos[0] - lefttop[0], lefttop[1] - pos[1]

        return [dx*interval[0], dy*interval[1]]

    def render(self, value=linearvalue) -> None:
        Range = value(self.range)
        interval = value(self.interval)
        self.value = value
        self.size = [
            abs(Range[0][0] - Range[0][1]) * interval[0],
            abs(Range[1][0] - Range[1][1]) * interval[1]
        ]

        self.body = pygame.Surface(self.size, pygame.SRCALPHA)
        self.rect = pygame.Rect(value(self.pos)+value(self.size))
        
        
        # render axis
        if (self.showaxis and self.axiswidth > 0):

            rrect(
                self.body, self.calcpos(( min(Range[0]), 0 )) + [self.size[0], self.axiswidth], self.axiscolor, 0.9
            )
            rrect(
                self.body, self.calcpos(( 0, max(Range[1]) )) + [self.axiswidth, self.size[1]], self.axiscolor, 0.9
            )

        # render equation

        for function in self.function:
            try:
            
                TYPE = function.get('type', '')
                color = function.get('color', [255, 0, 0])
                width = function.get('width', 3)
                points = []

                if (TYPE == 'equation'):
                    equation = function.get('equation', '')
                    if (equation == ''): continue
                    if ('=' in equation): equation = equation[equation.find('=')+1:]

                    for X in range(self.size[0]//self.renderstep):
                        x = X/interval[0]*self.renderstep + min(Range[0])
                        y = eval(value(equation))
                        points.append((x, y))

                elif (TYPE == 'points'):
                    points = function.get('points', [])

                    if (type(points) == str):
                        points = eval(value(points))
                        if (type(points) != list): points = []

                    else: points = []

                for i, p in enumerate(points[:-1]):
                    c = self.calcpos(p)
                    p2 = points[i+1]
                    pygame.draw.circle(self.body, color, (round(c[0]), round(c[1])), width//2)
                    drawLineWidth(
                        self.body, color, c, self.calcpos(p2), width
                    )

                if (len(points) == 1):
                    c = self.calcpos(points[0])
                    # print(distance((0, 0), points[0]))
                    pygame.draw.circle(self.body, color, (round(c[0]), round(c[1])), width)



            except Exception as e: print(e)

            continue




        return

    
    def draw(self, **kwargs) -> None:
        self.surface = kwargs.get('surface', self.surface)
        if (not self.surface): return
        
        value = kwargs.get('value', linearvalue)
        self.render(value)
        self.rect = pygame.Rect(value(self.pos)+value(self.size))
        return self.body