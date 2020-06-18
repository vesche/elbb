import pyautogui

x1 = 2722
y1 = 603
x2 = 2762
y2 = 611

img = pyautogui.screenshot(region=(x1, y1, x2-x1, y2-y1))
img.save('images/foo.png')