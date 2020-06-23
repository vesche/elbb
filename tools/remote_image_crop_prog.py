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

root = Tk()
root.geometry('1400x800')
root.configure(background='grey')

def get_coords(mouse):
    x = mouse.x
    y = mouse.y
    print(x, y)

def get_scrot():
    if os.path.exists('headless_scrot.png'):
        os.remove('headless_scrot.png')
    conn.run('python /tmp/headless_scrot.py')
    conn.get('/tmp/headless_scrot.png', 'headless_scrot.png')
    img = ImageTk.PhotoImage(Image.open('headless_scrot.png'))
    img_label = Label(root, image=img)
    img_label.photo = img
    img_label.place(x=0, y=0)

scrot_button = Button(root, text='scrot!', command=get_scrot)
scrot_button.place(x=1026, y=0)

root.bind("<Button 1>", get_coords)
root.mainloop()