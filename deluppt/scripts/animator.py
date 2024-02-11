import time, math, random
from deluppt.scripts.functions import *

class animator:
    def ease(x:float) -> float:
        return (x**2)/((2*(x**2-x)+1))
    
    def calculate(time, self, window, function):
        function = function.replace("$time", str(time))
        value = eval(function)
        return value
        
    def get_current(time, init, duration, start, end, value=linearvalue, ease:bool=False):
        if (time < init): return 
        elif (time > init+duration): return 
        if (duration == 0): return end
        if (duration < 0): return start
        
        start = value(start)
        end = value(end)
        if (type(start) != type(end)): return
        t = type(start)
        
        if (t == int):
            if (not ease):
                inclination = (end-start)/(duration)
                value = inclination * (time - init) + start
                return value
            else:
                value = start + (end-start)*animator.ease((time-init)/duration)
                return value
        
        elif (t in [list, tuple]):
            if (len(start) != len(end)): return
            result = []
            for s, e in zip(start, end):
                if (type(s) != type(e)): return
                result.append(animator.get_current(time, init, duration, s, e, value, ease))

            return t(result)
        
    def decode(time, self, window, animation:dict):
        function = animation.get('function', '')
        
        if (function): return animator.calculate(time, self, window, function)
        
        init = animation.get('init', 0)
        duration = animation.get('duration', 0)
        start = animation.get('start', 0)
        end = animation.get('end', 0)
        
        return animator.get_current(time, init, duration, start, end)