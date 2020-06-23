import os
import json

from tkinter import *
from fabric import Connection
from PIL import ImageTk, Image

with open('my.json') as f:
    config = json.loads(f.read())

conn = Connection(
    host=config['host'],
    user=config['user'],
    port=config['port'],
    connect_kwargs={'password': config['pass']}
)
conn.put('headless_scrot.py', '/tmp/headless_scrot.py')

n = 0
img, img_raw = None, None
PIN_1, PIN_2 = None, None
PIN_1_SELECTED, PIN_2_SELECTED = True, False
PIN_1_COORDS, PIN_2_COORDS = (0, 0), (0, 0)

root = Tk()
root.geometry('1400x800')
root.configure(background='grey')

canvas = Canvas(
    root,
    width=1024, height=768,
    borderwidth=0, highlightthickness=0
)

def get_coords(mouse):
    global PIN_1
    global PIN_2
    global PIN_1_SELECTED
    global PIN_2_SELECTED
    global PIN_1_COORDS
    global PIN_2_COORDS
    global canvas

    x = mouse.x
    y = mouse.y

    if PIN_1_SELECTED:
        PIN_1_SELECTED = False
        PIN_2_SELECTED = True
    elif PIN_2_SELECTED:
        PIN_1_SELECTED = True
        PIN_2_SELECTED = False

    if PIN_1_SELECTED:
        canvas.delete(PIN_1)
        canvas.delete(PIN_2)
        PIN_1 = canvas.create_rectangle(x-3, y-3, x+3, y+3, fill='red', width=0)
        PIN_1_COORDS = (x, y)
    elif PIN_2_SELECTED:
        canvas.delete(PIN_2)
        PIN_2 = canvas.create_rectangle(x-3, y-3, x+3, y+3, fill='red', width=0)
        PIN_2_COORDS = (x, y)

def get_scrot():
    global img
    global img_raw
    if os.path.exists('headless_scrot.png'):
        os.remove('headless_scrot.png')
    conn.run('python /tmp/headless_scrot.py')
    conn.get('/tmp/headless_scrot.png', 'headless_scrot.png')
    img_raw = Image.open('headless_scrot.png')
    img = ImageTk.PhotoImage(img_raw)
    canvas.create_image(512, 384, image=img)
    canvas.pack()

def crop_img(foo):
    img_raw.crop((*PIN_1_COORDS, *PIN_2_COORDS)).save('crop.png')

def save_img(foo):
    global n
    os.system(f'mv crop.png save-{n}.png')

scrot_button = Button(root, text='scrot', command=get_scrot)
scrot_button.place(x=0, y=0)

root.bind('<Button 1>', get_coords)
root.bind('<space>', crop_img)
root.bind('<Return>', save_img)

root.mainloop()
