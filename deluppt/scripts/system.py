import pygame, sys
import win32gui, win32con, win32api, subprocess, os
from threading import Thread

import ctypes

from deluppt.scripts.window import window


user32 = ctypes.windll.user32
FullScreen = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
DETACHED_PROCESS = 0x00000008
def wndProc(oldWndProc, draw_callback, hWnd, message, wParam, lParam):
    global window
    if message == win32con.WM_SIZE:
        draw_callback()
        win32gui.RedrawWindow(hWnd, None, None, win32con.RDW_INVALIDATE | win32con.RDW_ERASE)
    return win32gui.CallWindowProc(oldWndProc, hWnd, message, wParam, lParam)


class system:
    
    ppt = ''
    clock = pygame.time.Clock()
    moveable = True
    mouse_visible = False
    
    def event(events:list=[], display:window=None):
        
        for event in events:
            
            if (event.type == pygame.QUIT):
                pygame.quit()
                sys.exit()
                
            
            if (event.type == pygame.KEYUP):
                if (event.key == pygame.K_F11):
                    if (display == None): continue
                    
                    display.fullscreen()
                
                elif (event.key == pygame.K_F5):
                    if (display == None): continue
                    
                    i = display.index if (type(display.index) == int) else display.index[1]
                    display.load(system.ppt)
                    if (i < len(display.pages)): display.move_page(i, True)
                    
                elif (event.key in [pygame.K_SPACE, pygame.K_DOWN, pygame.K_RIGHT, pygame.K_UP, pygame.K_LEFT]):
                    system.moveable = True

                elif (event.key == pygame.K_LALT): pygame.mouse.set_visible(False or system.mouse_visible)
                
            if (event.type == pygame.KEYDOWN):
                if (event.key in [pygame.K_SPACE, pygame.K_DOWN, pygame.K_RIGHT] and system.moveable):
                    if (type(display.index) == int): display.move_page(display.index + 1)
                    elif (type(display.index) == tuple): display.move_page(display.index[1] + 1)
                    system.moveable = False
                    
                elif (event.key in [pygame.K_UP, pygame.K_LEFT] and system.moveable):
                    if (type(display.index) == int): display.move_page(display.index - 1)
                    elif (type(display.index) == tuple): display.move_page(display.index[1] - 1)
                    system.moveable = False
                
                elif (event.key == pygame.K_LALT): pygame.mouse.set_visible(True)
            
        if ("ctrl" in window.KeyboardState[0]):
            if ('m' in window.KeyboardState[2]):
                system.mouse_visible = system.mouse_visible == False
                pygame.mouse.set_visible(system.mouse_visible)
            elif ('o' in window.KeyboardState[2]):
                pid = subprocess.Popen([sys.executable, ".\\deluppt\\scripts\\color_chooser.py"],
                                    creationflags=DETACHED_PROCESS).pid
                
    def run(ppt:str|dict=""):
        system.ppt = ppt
        
        display = window()
        display.load(ppt)
        pygame.mouse.set_visible(False or system.mouse_visible)
        
        hwnd = pygame.display.get_wm_info()['window']
        oldWndProc = win32gui.SetWindowLong(hwnd, win32con.GWL_WNDPROC, lambda *args: wndProc(oldWndProc, display.update, *args))
        
        while True:
            events = pygame.event.get()
            
            system.event(events, display)
            display.update()