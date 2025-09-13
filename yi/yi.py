import tkinter as tk
from math import floor
from random import randint as rd
from time import time

colorMap = {}
scr = []
x = 9
y = 6
player_x = [x, x - 1, x - 2]
player_y = [y, y, y]
scr_x = 12
scr_y = 16
length = 3
score = 0
ax = rd(0, scr_x - 1)
ay = rd(0, scr_y - 1)
dx = 0
dy = 0
de = False
tm = time()
running = True
pause = False
delay = [0.5, 0.4, 0.35, 0.3, 0.2, 0.1, 0.08, 0.05, 0.02]
walls = {}
high = {}
scale = 20
direction = "right"
d1 = "right"
level = 7
success = False
recv = []
game_data: dict[str, list] = {}


def offline(map_name, lvl):
    global level, ax, ay, success, scr_x, scr_y, scale
    level = lvl
    try:
        exec('global colorMap\ncolorMap={' + open('color.txt').read() + '}')
    except FileNotFoundError:
        open('color.txt', 'w').write(''''bg': '#EEEEEE',
'button_text': '#000000',
'button_bg': '#FFFFFF',
'bar': '#0000FF',
'time': '#FFFFFF',
'head': '#DD7700',
'body': '#777700',
'dot': '#0000FF',
'apple': '#FF0000',
'end_text': '#FF0000',
'end_bg': '#000000',
'wall': '#777777',''')
        exec('global colorMap\ncolorMap={' + open('color.txt').read() + '}')
    for i_ in open(map_name).read().split('\n')[:-1]:
        walls[i_] = True
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

    a = tk.Tk()
    a.config(bg=colorMap['bg'])
    a.focus_force()
    a.resizable(False, False)
    while not success:
        for i_ in range(0, len(player_x), 1):
            if ax == player_x[i_] and ay == player_y[i_]:
                success = False
                ax = rd(0, scr_x - 1)
                ay = rd(0, scr_y - 1)
                break
        else:
            try:
                if walls[f'{ax} {ay}']:
                    ax = rd(0, scr_x - 1)
                    ay = rd(0, scr_y - 1)
                    continue
            except KeyError:
                pass
            success = True

    def paint(x1, y1, color):
        global scale
        b = tk.Label(a, bg=color)
        b.place(x=scale * x1, y=scale * y1, width=scale, height=scale)
        scr.append(b)

    def cls():
        for i in scr:
            i.destroy()

    def left():
        global direction, d1
        if d1 != "right" and not pause:
            direction = "left"

    def right():
        global direction, d1
        if d1 != "left" and not pause:
            direction = "right"

    def up():
        global direction, d1
        if d1 != "down" and not pause:
            direction = "up"

    def down():
        global direction, d1
        if d1 != "up" and not pause:
            direction = "down"

    def change1():
        global level
        if level == len(delay):
            level = 1
        else:
            level += 1
        lev.config(text=f"{level}")

    def change2():
        global level
        if level == 1:
            level = len(delay)
        else:
            level -= 1
        lev.config(text=f"{level}")

    def click_pause():
        global pause
        if pause:
            pause = False
            generate()
        else:
            pause = True

    def k(event):
        k0 = event.keysym
        if k0 == "d":
            right()
        elif k0 == "a":
            left()
        elif k0 == "w":
            up()
        elif k0 == "s":
            down()
        elif k0 == "space":
            click_pause()
        elif k0 == "Left":
            change2()
        elif k0 == "Right":
            change1()

    a.bind("<Key>", k)

    bar = tk.Label(a, bg=colorMap['bar'])
    bar.place(x=0, y=scale * scr_y, width=scale * scr_x, height=scale * 3)
    sc = tk.Label(a, text="0", bg=colorMap['button_bg'], fg=colorMap['button_text'], font=("微软雅黑", 10))
    sc.place(x=0, y=scale * (scr_y + 2), width=scale * 2, height=scale)
    lev = tk.Button(a, command=change1, text=f"{level}", bg=colorMap['button_bg'], fg=colorMap['button_text'])
    lev.place(x=scale * (scr_x - 1), y=(scr_y + 2) * scale, width=scale, height=scale)
    p = tk.Button(a, command=click_pause, bg=colorMap['button_bg'], fg=colorMap['button_text'], text="暂停")
    p.place(x=0, y=(scr_y + 1) * scale, width=scale * 2, height=scale)
    rt = tk.Label(a, text=f"{0}", bg=colorMap['dot'], font=("", 12), fg=colorMap['time'])

    def dot():
        global dx, dy, de, tm, success
        dx = rd(0, scr_x - 1)
        dy = rd(0, scr_y - 1)
        de = True
        tm = time()
        success = False
        while not success:
            for i in range(0, len(player_x), 1):
                if dx == player_x[i] and dy == player_y[i]:
                    success = False
                    dx = rd(0, scr_x - 1)
                    dy = rd(0, scr_y - 1)
                    break
            else:
                try:
                    if walls[f'{dx} {dy}']:
                        dx = rd(0, scr_x - 1)
                        dy = rd(0, scr_y - 1)
                        continue
                except KeyError:
                    pass
                success = True
        rt.place(x=dx * scale, y=dy * scale, width=scale, height=scale)
        rt.config(text="6")

    def dot2():
        global x, y, dx, dy, de, score
        dt = int(time() - tm)
        rt.config(text=f"{6 - dt}")
        if dt > 6:
            de = False
            rt.place_forget()
        if de and x == dx and y == dy:
            score += int(6 - dt) * 3
            sc.config(text=f"{score}")
            de = False
            rt.place_forget()

    def apple():
        global x, y, ax, ay, length, score, success
        if x == ax and y == ay:
            length += 1
            score += 1
            sc.config(text=f"{score}")
            if score % 6 == 0 and score != 0 and not de:
                dot()
            ax = rd(0, scr_x - 1)
            ay = rd(0, scr_y - 1)
            success = False
            while not success:
                for i in range(0, len(player_x), 1):
                    if ax == player_x[i] and ay == player_y[i]:
                        success = False
                        ax = rd(0, scr_x - 1)
                        ay = rd(0, scr_y - 1)
                        break
                else:
                    try:
                        if walls[f'{ax} {ay}']:
                            ax = rd(0, scr_x - 1)
                            ay = rd(0, scr_y - 1)
                            continue
                    except KeyError:
                        pass
                    success = True

    def gameover():
        global x, y, running
        flag = False
        try:
            if walls[f'{x} {y}']:
                running = False
                return
        except KeyError:
            pass
        for i in range(1, len(player_x), 1):
            if player_x[i] == x and player_y[i] == y:
                flag = True
        if flag:
            running = False

    def move(arg=None):
        if arg is not None:
            return
        global x, y, scr_x, scr_y, direction, length, d1
        if direction == "left":
            if x == 0:
                x = scr_x - 1
            else:
                x -= 1
        if direction == "right":
            if x == scr_x - 1:
                x = 0
            else:
                x += 1
        if direction == "up":
            if y == 0:
                y = scr_y - 1
            else:
                y -= 1
        if direction == "down":
            if y == scr_y - 1:
                y = 0
            else:
                y += 1
        d1 = direction
        player_x.insert(0, x)
        player_y.insert(0, y)
        try:
            player_x.pop(length)
            player_y.pop(length)
        except IndexError:
            pass
        a.after(0, generate, None)

    def generate(arg=None):
        if arg is not None:
            return
        global x, y, length, ax, ay, pause
        apple()
        dot2()
        gameover()
        cls()
        paint(ax, ay, colorMap['apple'])
        paint(player_x[0], player_y[0], colorMap['head'])
        for i in walls.keys():
            tmp = [int(j) for j in i.split(' ')]
            paint(*tmp, colorMap['wall'])
        for i in range(1, len(player_x), 1):
            paint(player_x[i], player_y[i], colorMap['body'])
        if running:
            if not pause:
                a.after(int(1000 * delay[level - 1]), move, None)
        else:
            text = "考试无分!"
            nam = map_name.split('.')[0]
            if score > high[nam]:
                text += "\n打破纪录！"
                high[nam] = score
                s = ''
                for i in high.keys():
                    s += f"'{i}' : {high[i]},\n"
                open("yihs.txt", "w").write(s[:-1])
            over = tk.Label(a, text=text, bg=colorMap['end_bg'], fg=colorMap['end_text'], font=("", 12))
            over.place(x=0.5 * scale * scr_x - 40, y=0.5 * scale * scr_y - 10, width=4 * scale, height=2 * scale)

    a.geometry(
        f"{scale * scr_x}x{scale * (scr_y + 3)}+{int(a.winfo_screenwidth() / 2 - 0.5 * scale * scr_x)}+"
        f"{int(a.winfo_screenheight() / 2 - 0.5 * scale * scr_y)}")
    a.title("贪吃易")
    l = tk.Button(a, text="←", command=left, bg=colorMap['button_bg'], fg=colorMap['button_text'])
    l.place(x=scale * (floor(scr_x / 2) - 1), y=scale * (scr_y + 1), width=scale, height=scale)
    r = tk.Button(a, text="→", command=right, bg=colorMap['button_bg'], fg=colorMap['button_text'])
    r.place(x=scale * (floor(scr_x / 2) + 1), y=scale * (scr_y + 1), width=scale, height=scale)
    u = tk.Button(a, text="↑", command=up, bg=colorMap['button_bg'], fg=colorMap['button_text'])
    u.place(x=scale * (floor(scr_x / 2)), y=scale * (scr_y), width=scale, height=scale)
    d = tk.Button(a, text="↓", command=down, bg=colorMap['button_bg'], fg=colorMap['button_text'])
    d.place(x=scale * (floor(scr_x / 2)), y=scale * (scr_y + 2), width=scale, height=scale)
    generate()

    a.mainloop()


def online(player_name, lvl):
    global level, recv, game_data, x, y, scale
    import socket
    import tkinter.messagebox as msg
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('127.0.0.1', 2048))
    client_data = {'ver': 1.0}

    def to_dict(s: str):
        cmd = 'global game_data\ngame_data='
        if not s.startswith('{'):
            cmd += '{'
        cmd += s
        if not s.endswith('}'):
            cmd += '}'
        exec(cmd)

    def receive():
        global recv
        try:
            tmp = client_socket.recv(1024).decode('utf-8')
            client_socket.setblocking(False)
            while True:
                try:
                    client_socket.settimeout(0.1)
                    more = client_socket.recv(1024).decode('utf-8')
                    if more == '':
                        break
                    tmp += more
                except socket.error or socket.timeout:
                    break
            client_socket.setblocking(True)
            tmp = tmp.split(' ')
            # print(tmp)
            recv = tmp
        except Exception as e:
            if e == ConnectionResetError:
                msg.showerror('错误', '连接已断开！')
                client_socket.close()

    def send(message, no_recv=False):
        tmp = message.split(' ')
        sd = {'cmd': tmp[0], 'optc': int(tmp[1])}
        sd['opt'] = tmp[2:2 + sd['optc']]
        sd['msg'] = ' '.join(i for i in tmp[2 + sd['optc']:])
        client_socket.send(str(sd).encode('utf-8'))
        if not no_recv:
            receive()

    client_socket.send(str(client_data).encode('utf-8'))
    receive()
    if recv[0] != 'ok':
        exit(1)

    send(f'game_join 2 {player_name} {lvl}')
    if recv[0] != 'ok':
        msg.showerror('错误', '无法加入游戏：'+recv[1])
        return
    x = int(recv[1])
    y = int(recv[2])
    map_name = "Classic.map"
    level = lvl
    try:
        exec('global colorMap\ncolorMap={' + open('color.txt').read() + '}')
    except FileNotFoundError:
        open('color.txt', 'w').write(''''bg': '#EEEEEE',
    'button_text': '#000000',
    'button_bg': '#FFFFFF',
    'bar': '#0000FF',
    'time': '#FFFFFF',
    'head': '#DD7700',
    'body': '#777700',
    'dot': '#0000FF',
    'apple': '#FF0000',
    'end_text': '#FF0000',
    'end_bg': '#000000',
    'wall': '#777777',''')
        exec('global colorMap\ncolorMap={' + open('color.txt').read() + '}')
    for i_ in open(map_name).read().split('\n')[:-1]:
        walls[i_] = True

    a = tk.Tk()
    a.config(bg=colorMap['bg'])
    a.attributes('-toolwindow', True)
    a.attributes('-topmost', True)
    a.focus_force()
    a.resizable(False, False)

    def paint(x1, y1, color):
        x1 = int(x1)
        y1 = int(y1)
        global scale
        b = tk.Label(a, bg=color)
        b.place(x=scale * x1, y=scale * y1, width=scale, height=scale)
        scr.append(b)

    def cls():
        for i in scr:
            i.destroy()

    def left():
        global direction
        if d1 != "right":
            direction = "left"

    def right():
        global direction
        if d1 != "left":
            direction = "right"

    def up():
        global direction
        if d1 != "down":
            direction = "up"

    def down():
        global direction
        if d1 != "up":
            direction = "down"

    def k(event):
        k0 = event.keysym
        if k0 == "d":
            right()
        elif k0 == "a":
            left()
        elif k0 == "w":
            up()
        elif k0 == "s":
            down()

    a.bind("<Key>", k)

    bar = tk.Label(a, bg=colorMap['bar'])
    bar.place(x=0, y=scale * scr_y, width=scale * scr_x, height=scale * 3)
    sc = tk.Label(a, text="0", bg=colorMap['button_bg'], fg=colorMap['button_text'], font=("微软雅黑", 10))
    sc.place(x=0, y=scale * (scr_y + 2), width=scale * 2, height=scale)
    lev = tk.Label(a, text=f"{level}", bg=colorMap['button_bg'], fg=colorMap['button_text'])
    lev.place(x=scale * (scr_x - 1), y=(scr_y + 2) * scale, width=scale, height=scale)

    def gameover():
        global running
        running = recv[0] == 'info'

    def move(arg=None):
        if arg is not None:
            return
        global x, y, d1
        if direction == "left":
            if x == 0:
                x = scr_x - 1
            else:
                x -= 1
        elif direction == "right":
            if x == scr_x - 1:
                x = 0
            else:
                x += 1
        elif direction == "up":
            if y == 0:
                y = scr_y - 1
            else:
                y -= 1
        elif direction == "down":
            if y == scr_y - 1:
                y = 0
            else:
                y += 1
        d1 = direction
        send(f'game_player 2 {x} {y}')
        a.after(0, generate, None)

    def generate(arg=None):
        if arg is not None:
            return
        global x, y, length, ax, ay, dx, dy, score
        send(f'game_get 2 {player_name} {lvl}')
        gameover()
        if not running:
            text = "考试无分!"
            over = tk.Label(a, text=text, bg=colorMap['end_bg'], fg=colorMap['end_text'], font=("", 12))
            over.place(x=0.5 * scale * scr_x - 40, y=0.5 * scale * scr_y - 10, width=4 * scale, height=2 * scale)
            return
        cls()
        s = ''
        for i in recv[1:]:
            s += i+' '
        to_dict(s[:-1])
        ax = game_data['apple'][0]
        ay = game_data['apple'][1]
        tsc = game_data['dot'][2]
        if tsc > 0:
            dx = game_data['dot'][0]
            dy = game_data['dot'][1]
            dt = tk.Label(a, text=str(tsc), bg=colorMap['dot'], font=("", 12), fg=colorMap['time'])
            dt.place(x=dx*scale, y=dy*scale, width=scale, height=scale)
            scr.append(dt)
        paint(ax, ay, colorMap['apple'])
        for i in walls.keys():
            paint(*(i.split(' ')), colorMap['wall'])
        for p in game_data.keys():
            if p.startswith('p_'):
                tmp = game_data[p]
                color = tmp[0]
                if color == 'gameover':
                    continue
                name = tmp[1]
                if name == player_name:
                    score += int(tmp[2])
                    sc.config(text=str(score))
                head = tk.Label(a, text=name, bg=color, fg='black', font=('', 6))
                head.place(x=int(tmp[3][0]*scale), y=int(tmp[3][1]*scale), width=scale, height=scale)
                scr.append(head)
                for i in range(4, len(tmp)):
                    paint(*tmp[i], color)
        a.after(int(1000 * delay[level - 1]), move, None)

    a.geometry(
        f"{scale * scr_x}x{scale * (scr_y + 3)}+{int(a.winfo_screenwidth() / 2 - 0.5 * scale * scr_x)}+"
        f"{int(a.winfo_screenheight() / 2 - 0.5 * scale * scr_y)}")
    a.title(f"联机贪吃易 - {player_name}")
    l = tk.Button(a, text="←", command=left, bg=colorMap['button_bg'], fg=colorMap['button_text'])
    l.place(x=scale * (floor(scr_x / 2) - 1), y=scale * (scr_y + 1), width=scale, height=scale)
    r = tk.Button(a, text="→", command=right, bg=colorMap['button_bg'], fg=colorMap['button_text'])
    r.place(x=scale * (floor(scr_x / 2) + 1), y=scale * (scr_y + 1), width=scale, height=scale)
    u = tk.Button(a, text="↑", command=up, bg=colorMap['button_bg'], fg=colorMap['button_text'])
    u.place(x=scale * (floor(scr_x / 2)), y=scale * (scr_y), width=scale, height=scale)
    d = tk.Button(a, text="↓", command=down, bg=colorMap['button_bg'], fg=colorMap['button_text'])
    d.place(x=scale * (floor(scr_x / 2)), y=scale * (scr_y + 2), width=scale, height=scale)
    generate()

    a.mainloop()


if __name__ == '__main__':
    online(input('name:'), 7)
