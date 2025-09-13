import os
from tkinter import Tk, Button, ttk, Label, Entry, messagebox as msg

import genMp
import yi

high = {}
try:
    exec('global high\nhigh={' + open('yihs.txt').read() + '}')
except FileNotFoundError:
    open("yihs.txt", "w").write(''''Classic' : 0,
'Box' : 0,
'Tunnel' : 0,
'Mill' : 0,
'Rails' : 0,
'Apartment' : 0,''')
    exec('global high\nhigh={' + open('yihs.txt').read() + '}')
sm = 'Classic.map'


def sf(event=None):
    if event is None:
        return
    global sm
    sm = slct.get()
    if sm == 'Classic.online':
        hs.config(text='联机模式不计最高分')
        lvl.set(9)
    else:
        hs.config(text=f'此地图最高分:{high[sm[:-4]]}')


level = 7


def lf(event):
    if event is None:
        return
    global level
    level = int(lvl.get())


def launch():
    name = player.get()
    if name == '':
        msg.showerror('错误', '名字不能为空')
    w.destroy()
    w.quit()
    if sm == 'Classic.online':
        yi.online(name, level)
    else:
        yi.offline(sm, level)


def mk_map():
    global maps
    tmp = genMp.main()[:-4]
    high[tmp] = 0
    maps = [i for i in os.listdir('.') if i.split('.')[-1] == 'map']
    open('yihs.txt', 'a').write("'" + tmp + "' : 0,\n")
    slct.config(values=maps)


w = Tk(className='yiLauncher')
w.geometry('320x230')
maps = [i for i in os.listdir('.') if i.split('.')[-1] == 'map']
maps.append('Classic.online')
lvls = [str(i) for i in range(1, 10)]
hs = Label(text=f'此地图最高分:{high[sm[:-4]]}')
hs.place(x=160, y=10)
Label(text='地图：').place(x=20, y=10)
slct = ttk.Combobox(values=maps, state='readonly')
slct.set(sm)
slct.place(x=60, y=10, width=100)
slct.bind('<<ComboboxSelected>>', sf)
Label(text='难度：').place(x=20, y=60)
lvl = ttk.Combobox(values=lvls, state='readonly')
lvl.set('7')
lvl.place(x=60, y=60, width=100)
lvl.bind('<<ComboboxSelected>>', lf)
Label(text='名称：').place(x=20, y=110)
player = Entry()
player.place(x=60, y=110, width=100)

ok = Button(text='确定', command=launch)
ok.place(x=60, y=160, width=100)

custom = Button(text='制作地图', command=mk_map)
custom.place(x=160, y=160, width=100)

w.mainloop()
