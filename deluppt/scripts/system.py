import pygame, sys
import win32gui, win32con, win32api

import ctypes

from deluppt.scripts.window import window


user32 = ctypes.windll.user32
FullScreen = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)

def wndProc(oldWndProc, draw_callback, hWnd, message, wParam, lParam):
    global window
    if message == win32con.WM_SIZE:
        draw_callback()
        win32gui.RedrawWindow(hWnd, None, None, win32con.RDW_INVALIDATE | win32con.RDW_ERASE)
    return win32gui.CallWindowProc(oldWndProc, hWnd, message, wParam, lParam)


class system:
    
    ppt = ''
    clock = pygame.time.Clock()
    pointer = pygame.SYSTEM_CURSOR_ARROW
    
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
                    
                    display.load(system.ppt)

            if (event.type == pygame.KEYDOWN):
                if (event.key in [pygame.K_SPACE, pygame.K_DOWN, pygame.K_RIGHT] ):
                    if (type(display.index) == int): display.move_page(display.index + 1)
                    if (type(display.index) == tuple): display.move_page(display.index[1] + 1)
                    
                elif (event.key in [pygame.K_UP, pygame.K_LEFT] ):
                    if (type(display.index) == int): display.move_page(display.index - 1)
                    if (type(display.index) == tuple): display.move_page(display.index[1] - 1)
                
    def run(ppt:str|dict=""):
        system.ppt = ppt
        
        display = window()
        display.load(ppt)
        
        hwnd = pygame.display.get_wm_info()['window']
        oldWndProc = win32gui.SetWindowLong(hwnd, win32con.GWL_WNDPROC, lambda *args: wndProc(oldWndProc, display.update, *args))
        
        while True:
            events = pygame.event.get()
            
            system.event(events, display)
            display.update()