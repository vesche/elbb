#!/usr/bin/env python

import os
import sys
import pyautogui

mouse_cmd = 'xdotool getmouselocation --shell'


def capture_mouse():
    input('Press ENTER to capture...')
    mouse_output = os.popen(mouse_cmd).read()
    for line in mouse_output.splitlines():
        var, n = line.split('=')
        if var == 'X':
            x = int(n)
        elif var == 'Y':
            y = int(n)
    return (x, y)


def main():
    if len(sys.argv) < 2:
        print('Usage: ./get_image.py <filename>')
        sys.exit(1)

    filename = sys.argv[1]

    x1, y1 = capture_mouse()
    print(x1, y1)
    x2, y2 = capture_mouse()
    print(x2, y2)

    img = pyautogui.screenshot(region=(x1, y1, x2-x1, y2-y1))
    img.save('images/' + filename)


if __name__ == '__main__':
    main()
