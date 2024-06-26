import time, math, random
from deluppt.scripts.functions import *

class animator:
    def ease(x:float, amount=1, ease_se=(1, 1)) -> float:
        ease_se = tuple(ease_se)
        x = min(max(0, x), 1)
        a = amount
        
        if (ease_se == (1, 1)):
            if (x <= amount/3): return 9/(6*a-2*a**2)*x**2
            elif (x >= 1-amount/3): return -9/(6*a-2*a**2)*(x-1)**2+1
            else: return 3/(3-a)*(x-a/3)+a/(6-2*a)
            
        elif (ease_se == (0, 1)):
            if (x <= 1-amount/3): return 6/(6-a)*x
            else: return -9/(6*a-a**2)*(x-1)**2+1
            
        elif (ease_se == (1, 0)):
            if (x <= amount/3): return 9/(6*a-a**2)*x**2
            else: return 6/(6-a)*(x-a/3)+a/(6-a)
        else: return x
    
    def calculate(time, self, window, function):
        function = function.replace("$time", str(time))
        value = eval(function)
        return value
        
    def get_current(time, init, duration, start, end, value=linearvalue, ease:bool=False, ease_amount:float=1, ease_se=(1, 1)):
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
                value = start + (end-start)*animator.ease((time-init)/duration, ease_amount, ease_se)
                return value
        
        elif (t in [list, tuple]):
            if (len(start) != len(end)): return
            result = []
            for s, e in zip(start, end):
                if (type(s) != type(e)): return
                result.append(animator.get_current(time, init, duration, s, e, value, ease, ease_amount, ease_se))

            return t(result)
        
    def decode(time, self, window, animation:dict):
        function = animation.get('function', '')
        
        if (function): return animator.calculate(time, self, window, function)
        
        init = animation.get('init', 0)
        duration = animation.get('duration', 0)
        start = animation.get('start', 0)
        end = animation.get('end', 0)
        
        return animator.get_current(time, init, duration, start, end)