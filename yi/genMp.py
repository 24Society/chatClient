from tkinter import Tk, Button, Entry

bl = []
flag = {}
wall = []
cnt = 0
map_n = ''


def main():
    global bl, flag, wall, cnt, map_n
    w = Tk(className='制作地图')
    w.geometry('240x340')
    fn = Entry(w)
    fn.place(x=0, y=0, width=100)

    def gen(x, y, i):
        def clk():
            tmp = f'{x} {y}'
            if flag[tmp]:
                wall.remove(tmp)
                flag[tmp] = False
                bl[i].config(bg='white')
            else:
                wall.append(tmp)
                flag[tmp] = True
                bl[i].config(bg='red')

        return clk

    def out():
        global map_n
        map_n = fn.get() + ('.map' if fn.get()[-4:] != '.map' else '')
        with open(map_n, 'w') as f:
            for i in wall:
                f.write(i + '\n')
        w.quit()
        w.destroy()

    for x_ in range(12):
        for y_ in range(16):
            flag[f'{x_} {y_}'] = False
            b = Button(w, command=gen(x_, y_, cnt))
            b.place(x=x_ * 20, y=y_ * 20 + 20, width=20, height=20)
            b.config(bg='white')
            bl.append(b)
            cnt += 1

    ok = Button(w, text='保存', command=out)
    ok.place(x=100, y=0, width=40, height=20)

    w.mainloop()
    return map_n


if __name__ == '__main__':
    main()
