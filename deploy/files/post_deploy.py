import os
import time
import pyautogui
import Xlib.display

from pyvirtualdisplay.smartdisplay import SmartDisplay

display = SmartDisplay(visible=0, size=(1280, 1024))
display.start()
pyautogui._pyautogui_x11._display = Xlib.display.Display(':99')
pyautogui.FAILSAFE = False

def clicker(x, y):
    pyautogui.moveXo(x, y)
    pyautogui.click()
    time.sleep(1)

# select server
clicker(459, 475)

# click OK
clicker(820, 629)

# click No
clicker(712, 551)

# click OK
clicker(778, 547)

# click Yes
clicker(944, 549)

# click Save
clicker(855, 669)

# scroll down, wait, hit Accept
for _ in range(30):
    pyautogui.press('down')
time.sleep(20)
clicker(624, 768)

# click screen again to drop into Login
pyautogui.click()