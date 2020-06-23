import os
import time
import pyautogui
import Xlib.display

pyautogui._pyautogui_x11._display = Xlib.display.Display(
    os.environ['DISPLAY']
)
pyautogui.FAILSAFE = False
img = pyautogui.screenshot(region=(128, 128, 1024, 768))
img.save('/tmp/headless_scrot.png')