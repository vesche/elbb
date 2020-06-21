import pyautogui

x1 = 2020
y1 = 1036
x2 = 2059
y2 = 1077

img = pyautogui.screenshot(region=(x1, y1, x2-x1, y2-y1))
img.save('foo.png')