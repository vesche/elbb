import os
import time
import pyautogui
import Xlib.display

from pyvirtualdisplay.smartdisplay import SmartDisplay

display = SmartDisplay(visible=0, size=(1280, 1024))
display.start()
pyautogui._pyautogui_x11._display = Xlib.display.Display(':99')
pyautogui.FAILSAFE = False

# select server
pyautogui.moveTo(459, 475)
pyautogui.click()
time.sleep(1)

# click OK
pyautogui.moveTo(820, 629)
pyautogui.click()
time.sleep(1)

# click No
pyautogui.moveTo(712, 551)
pyautogui.click()
time.sleep(1)

# click OK
pyautogui.moveTo(778, 547)
pyautogui.click()
time.sleep(1)

# click Yes
pyautogui.moveTo(944, 549)
pyautogui.click()
time.sleep(1)