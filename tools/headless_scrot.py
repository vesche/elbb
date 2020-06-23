import mss
import mss.tools

region = {'top':128, 'left':128, 'width':1024, 'height':768}

with mss.mss() as sct:
    img = sct.grab(region)
    mss.tools.to_png(img.rgb, img.size, output='/tmp/headless_scrot.png')
