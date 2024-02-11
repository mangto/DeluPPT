from pathlib import Path

from deluppt.scripts.system import system
from deluppt.scripts.window import window
from deluppt.scripts.imageloader import imageloader
from deluppt.scripts.objects import *
from deluppt.scripts.functions import *
from deluppt.scripts.keyboard import *
from deluppt.scripts.styler import ApplyStyle
from deluppt.scripts.transition import *
from deluppt.scripts.csys import *


######################### Complete Loading #########################

path = Path(__file__).parent.absolute()

with open(str(path)+"\\greeting.txt", "r", encoding="utf8") as file:
    __greeting__ = file.read()

print(__greeting__)