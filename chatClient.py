import socket
import threading
from datetime import datetime
from os import system, path
from re import sub
from time import sleep
from tkinter import font, Tk, Text, Scrollbar, Menu, Button, DISABLED, NORMAL, Label, Entry, messagebox as msg, \
    BooleanVar, Checkbutton, IntVar


def refresh(s: socket.socket):
    s.setblocking(False)
    while True:
        try:
            s.recv(1024)
        except socket.error:
            break
    s.setblocking(True)


def center(window: Tk, x=210, y=120):
    width = window.winfo_screenwidth()
    height = window.winfo_screenheight()
    center_x = int((width - x) / 2)
    center_y = int((height - y) / 2)
    window.geometry(f'{x}x{y}+{center_x}+{center_y}')


tmp_dict = {}


def to_dict(s: str) -> dict:
    cmd = 'global tmp_dict\ntmp_dict='
    if not s.startswith('{'):
        cmd += '{'
    cmd += s
    if not s.endswith('}'):
        cmd += '}'
    exec(cmd)
    return tmp_dict


loc_settings = to_dict(open('localSettings.txt', 'r').read())
HOST = loc_settings['def_ip']
PORT = int(loc_settings['def_port'])
client_data = {'ver': 1.2}


def local_setting():
    loc = Tk()
    loc.title(f'本地设置 - v{client_data['ver']}客户端')
    loc.attributes('-topmost', True)
    center(loc)
    Label(loc, text='默认ip：').place(x=10, y=10)
    def_ip = Entry(loc)
    def_ip.insert(0, loc_settings['def_ip'])
    def_ip.place(x=70, y=10, width=120)
    Label(loc, text='默认端口：').place(x=10, y=40)
    def_port = Entry(loc)
    def_port.insert(0, loc_settings['def_port'])
    def_port.place(x=70, y=40, width=120)

    def save():
        loc_settings['def_ip'] = def_ip.get()
        loc_settings['def_port'] = def_port.get()
        with open('localSettings.txt', 'w') as f:
            for i in loc_settings.keys():
                f.write(f"'{i}':'{loc_settings[i]}',\n")
        loc.destroy()

    def update():
        system('if exist D:\\24chat rd /s /q D:\\24chat > nul')
        system('md D:\\24chat > nul')
        system('ftp -n -s:update.txt > nul')
        if path.exists('D:\\24chat\\chatClient.py'):
            msg.showinfo('喜报', '已将最新版本下载到D:\\24chat\n请自行前往安装')
        else:
            msg.showerror('错误', '安装失败！无法正常从ftp获取最新版，请稍后重试')

    Button(loc, text='保存', command=save).place(x=10, y=80, width=60, height=20)
    Button(loc, text='取消', command=loc.destroy).place(x=80, y=80, width=60, height=20)
    Button(loc, text='更新', command=update).place(x=150, y=80, width=60, height=20)

    loc.mainloop()


client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    client_socket.connect((HOST, PORT))
except ConnectionRefusedError:
    if msg.askyesno('错误', '无法连接至服务器！\n是否进入离线模式？'):
        local_setting()
        exit(0)
    else:
        client_socket.close()
        exit(0)

client_socket.send(str(client_data).encode('utf-8'))
_recv = client_socket.recv(1024).decode('utf-8').split(' ')


def send(message):
    tmp = message.split(' ')
    sd = {'cmd': tmp[0], 'optc': int(tmp[1])}
    sd['opt'] = tmp[2:2 + sd['optc']]
    sd['msg'] = ' '.join(i for i in tmp[2 + sd['optc']:])
    client_socket.send(str(sd).encode('utf-8'))


if _recv[0] == 'refused':
    msg.showerror('错误', _recv[1])
    client_socket.close()
    if msg.askyesno('无法连接', '是否进入离线模式？'):
        local_setting()
    exit(0)
else:
    msg.showinfo('喜报', '成功连接到服务器')

win = Tk()
win.title('登录')
win.attributes('-topmost', True)
win.focus_force()
center(win)
Label(win, text='用户名：').place(x=10, y=10)
usr = Entry(win)
usr.place(x=70, y=10, width=120)
usr.focus_set()
Label(win, text='密码：').place(x=10, y=40)
pwd = Entry(win, show='*')
pwd.place(x=70, y=40, width=120)
var = BooleanVar()
show_pwd = Checkbutton(win, text='显示密码', variable=var)
show_pwd.place(x=70, y=60)
logged = False
usr_settings = {}
usrname = ''
passwd = ''
group_name = 'public'


def modify_show_pwd():
    if var.get():
        pwd.config(show='')
    else:
        pwd.config(show='*')


def log():
    global logged, usrname, passwd, usr_settings
    if usr.get() == '':
        win.attributes('-topmost', False)
        msg.showerror('错误', '请输入用户名！')
        win.attributes('-topmost', True)
        return
    login = f'log 2 {usr.get()} {pwd.get()}'
    send(login)
    tmp = client_socket.recv(1024).decode('utf-8').split(' ')
    cmd = tmp[0]
    if cmd == 'ok':
        logged = True
        usr_settings = to_dict(' '.join(tmp[1:]))
        win.attributes('-topmost', False)
        msg.showinfo('喜报', '登录成功！')
        win.attributes('-topmost', True)
        usrname = usr.get()
        passwd = pwd.get()
        win.destroy()
    else:
        win.attributes('-topmost', False)
        msg.showerror('错误', f'登录失败:{tmp[1]}')
        win.attributes('-topmost', True)


def reg():
    global logged, usrname, passwd, usr_settings
    if usr.get() == '':
        win.attributes('-topmost', False)
        msg.showerror('错误', '请输入用户名！')
        win.attributes('-topmost', True)
        return
    if pwd.get() == '':
        win.attributes('-topmost', False)
        msg.showerror('错误', '请输入密码！')
        win.attributes('-topmost', True)
        return
    regedit = f'reg 2 {usr.get()} {pwd.get()}'
    send(regedit)
    tmp = client_socket.recv(1024).decode('utf-8').split(' ')
    cmd = tmp[0]
    uid = tmp[1]
    if cmd == 'ok':
        logged = True
        win.attributes('-topmost', False)
        msg.showinfo('喜报', f'注册成功，已自动登录！\n你的id是 {uid}')
        win.attributes('-topmost', True)
        usr_settings = to_dict(' '.join(tmp[2:]))
        usrname = usr.get()
        passwd = pwd.get()
        win.destroy()
    else:
        win.attributes('-topmost', False)
        msg.showerror('错误', f'注册失败:{tmp[1]}')
        win.attributes('-topmost', True)


show_pwd.config(command=modify_show_pwd)
Button(win, text='确定', command=log).place(x=40, y=90, width=60, height=20)
Button(win, text='注册', command=reg).place(x=120, y=90, width=60, height=20)

win.mainloop()

if not logged:
    if msg.askyesno('未登录', '是否要进入离线模式？'):
        local_setting()
    exit(0)

win = Tk()
win.title(f'聊天窗口 - {usrname} in {group_name} (v{client_data['ver']})')
center(win, 500, 600)
win.resizable(width=True, height=False)
recv_msg = Text(win, width=67, height=40)
send_msg = Text(win, width=60, height=4)

font2 = font.Font(family='Times_New_Roman', size=12)
recv_msg.tag_config('normal', foreground='black', font=font2)
recv_msg.tag_config('highlight', foreground='black', background='lightgreen', font=font2)
ys1 = Scrollbar(win, command=send_msg.yview)
ys2 = Scrollbar(win, command=recv_msg.yview)
send_msg['yscrollcommand'] = ys1.set
recv_msg['yscrollcommand'] = ys2.set
recv_msg['state'] = DISABLED
cmd_recv = ''
running = True


def receive_messages():
    global cmd_recv
    while running:
        try:
            # refresh(client_socket)
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
            cmd = tmp[0]
            if cmd == 'message':
                send_name = tmp[1]
                send_id = tmp[2]
                message = ' '.join(tmp[3:])
                recv_msg['state'] = NORMAL
                if f'@{usrname} ' in message or f'@{usrname}\n' in message:
                    tag = 'highlight'
                else:
                    tag = 'normal'
                recv_msg.insert('end', f'[{send_name}' +
                                (f'(id:{send_id})' if usr_settings['show_uid'] else '') +
                                f'] {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}\n', tag)
                for i in message.split('\n'):
                    recv_msg.insert('end', '  ' + i + '\n', tag)
                recv_msg['state'] = DISABLED
                recv_msg.see('end')
            elif cmd == 'history':
                recv_msg['state'] = NORMAL
                for message in ' '.join(tmp[1:]).split('\0'):
                    if not usr_settings['show_uid']:
                        message = sub(r'\(id:(.*?)\)', '', message)
                    if f'@{usrname} ' in message or f'@{usrname}\n' in message:
                        tag = 'highlight'
                    else:
                        tag = 'normal'
                    recv_msg.insert('end', message, tag)
                recv_msg['state'] = DISABLED
                recv_msg.see('end')
            else:
                cmd_recv = ' '.join(i for i in tmp)
        except Exception as e:
            if e == ConnectionResetError:
                msg.showerror('错误', '连接已断开！')
                client_socket.close()
                break
            else:
                break


def load():
    recv_msg['state'] = NORMAL
    recv_msg.delete('1.0', 'end')
    send(f'history 1 {group_name}')
    recv_msg['state'] = DISABLED


receive_thread = threading.Thread(target=receive_messages)
receive_thread.start()

load()


def check():
    global cmd_recv
    send('check 0')
    tmpi = 0
    while cmd_recv == '' and tmpi < 10:
        sleep(0.1)
        tmpi += 1
    if tmpi == 10:
        msg.showerror('错误', '响应超时')
        return
    recv = cmd_recv.split(' ')
    if recv[0] == 'info':
        if float(recv[1]) == client_data['ver']:
            msg.showinfo('喜报', '您使用的是最新版本')
        else:
            msg.showwarning('警告', '您使用的不是最新版本，尽管目前仍可兼容，\n还请尽快在本地设置处更新')
    cmd_recv = ''


def send_message():
    tmp = send_msg.get('1.0', 'end').strip()
    if tmp == '':
        msg.showwarning('警告', '不可发送空内容')
        return
    send(f'message 1 {group_name} {tmp}\n')
    send_msg.delete('1.0', 'end')


def modify_name():
    mod_n = Tk()
    mod_n.title('更改用户名')
    mod_n.attributes('-topmost', True)
    mod_n.focus_force()
    center(mod_n)
    Label(mod_n, text='新用户名：').place(x=10, y=10)
    new_name = Entry(mod_n)
    new_name.place(x=70, y=10, width=120)
    new_name.focus_set()

    def save():
        global usrname, cmd_recv
        send(f'name 1 {new_name.get()}')
        tmpi = 0
        while cmd_recv == '' and tmpi < 10:
            sleep(0.1)
            tmpi += 1
        if tmpi == 10:
            mod_n.attributes('-topmost', False)
            msg.showerror('错误', '响应超时')
            mod_n.attributes('-topmost', True)
            return
        recv = cmd_recv.split(' ')
        cmd_recv = ''
        if recv[0] == 'ok':
            usrname = new_name.get()
            win.title(f'聊天窗口 - {usrname} in {group_name}')
            mod_n.attributes('-topmost', False)
            msg.showinfo('喜报', '已成功修改为此用户名')
            mod_n.attributes('-topmost', True)
            mod_n.destroy()
        else:
            mod_n.attributes('-topmost', False)
            msg.showerror('错误', '无法更改为此用户名：' + recv[1])
            mod_n.attributes('-topmost', True)

    Button(mod_n, text='确定', command=save).place(x=40, y=80, width=60, height=20)
    Button(mod_n, text='取消', command=mod_n.destroy).place(x=120, y=80, width=60, height=20)

    mod_n.mainloop()


def modify_password():
    mod_p = Tk()
    mod_p.title('更改密码')
    mod_p.attributes('-topmost', True)
    mod_p.focus_force()
    center(mod_p, x=240)
    Label(mod_p, text='旧密码：').place(x=10, y=10)
    old_pwd = Entry(mod_p, show='*')
    old_pwd.place(x=70, y=10, width=120)
    old_pwd.focus_set()
    var1 = BooleanVar(mod_p)
    show_old_pwd = Checkbutton(mod_p, text='显示旧密码', variable=var1)
    show_old_pwd.place(x=130, y=10)
    Label(mod_p, text='新密码：').place(x=10, y=40)
    new_pwd = Entry(mod_p, show='*')
    new_pwd.place(x=70, y=40, width=120)
    var2 = BooleanVar(mod_p)
    show_new_pwd = Checkbutton(mod_p, text='显示新密码', variable=var2)
    show_new_pwd.place(x=130, y=40)

    def modify_show_old_pwd():
        if var1.get():
            old_pwd.config(show='')
        else:
            old_pwd.config(show='*')

    def modify_show_new_pwd():
        if var2.get():
            new_pwd.config(show='')
        else:
            new_pwd.config(show='*')

    def save():
        global passwd, cmd_recv
        old = old_pwd.get()
        passwd = new_pwd.get()
        send(f'pwd 2 {old} {passwd}')
        tmpi = 0
        while cmd_recv == '' and tmpi < 10:
            sleep(0.1)
            tmpi += 1
        if tmpi == 10:
            mod_p.attributes('-topmost', False)
            msg.showerror('错误', '响应超时')
            mod_p.attributes('-topmost', True)
            return
        recv = cmd_recv.split(' ')
        cmd_recv = ''
        if recv[0] == 'ok':
            mod_p.attributes('-topmost', False)
            msg.showinfo('喜报', '已成功修改为此密码')
            mod_p.attributes('-topmost', True)
            mod_p.destroy()
        else:
            mod_p.attributes('-topmost', False)
            msg.showerror('错误', '无法更改为此密码：' + recv[1])
            mod_p.attributes('-topmost', True)

    show_old_pwd.config(command=modify_show_old_pwd)
    show_new_pwd.config(command=modify_show_new_pwd)
    Button(mod_p, text='确定', command=save).place(x=40, y=80, width=60, height=20)
    Button(mod_p, text='取消', command=mod_p.destroy).place(x=120, y=80, width=60, height=20)

    mod_p.mainloop()


def get_user_info():
    global cmd_recv
    send(f'info 1 user')
    tmpi = 0
    while cmd_recv == '' and tmpi < 10:
        sleep(0.1)
        tmpi += 1
    if tmpi == 10:
        msg.showerror('错误', '响应超时')
        return
    cmd = cmd_recv.split(' ')[0]
    if cmd == 'info':
        usr_info = to_dict(cmd_recv[5:])
        msg.showinfo('用户信息', '\n'.join(f'{i}:{usr_info[i]},' for i in usr_info.keys()))
    else:
        msg.showerror('错误', '获取信息失败，请稍后重试')
    cmd_recv = ''


def cancel():
    global cmd_recv, running
    if msg.askokcancel('警告', '注销后你的一切信息将被删除，但你发送的信息不会被清理'):
        send('cancel 0')
        tmpi = 0
        recv = cmd_recv.split(' ')
        while recv[0] == '' and tmpi < 10:
            sleep(0.1)
            tmpi += 1
            recv = cmd_recv.split(' ')
        if tmpi == 10:
            msg.showerror('错误', '响应超时')
            return
        if recv[0] == 'ok':
            msg.showinfo('提示', '已注销此用户，自动退出登录')
            win.destroy()
            running = False
        else:
            msg.showerror('错误', '注销失败:' + recv[1])
        cmd_recv = ''


def set_remember_me():
    if not usr_settings['remember_me']:
        if not msg.askyesno('警告', '记住密码后，任何人都可以通过仅输入您的用户名\n'
                            '来登录您的账号，无论密码是否正确，确定要启用吗？'):
            return
    else:
        msg.showinfo('提示', '已取消记住密码')
    usr_settings['remember_me'] = not usr_settings['remember_me']
    remember_me.set(usr_settings['remember_me'])
    send('remember 0')


def set_show_uid():
    send(f'show_uid 0')
    if usr_settings['show_uid']:
        msg.showinfo('提示', '已设置为不显示uid')
    else:
        msg.showinfo('提示', '已设置为显示uid')
    usr_settings['show_uid'] = not usr_settings['show_uid']
    show_uid.set(usr_settings['show_uid'])
    load()


def start_vote():
    start_v = Tk()
    start_v.title('发起投票')
    start_v.attributes('-topmost', True)
    start_v.focus_force()
    center(start_v)
    Label(start_v, text='投票主题：').place(x=10, y=10)
    vote_title = Entry(start_v)
    vote_title.place(x=70, y=10, width=120)
    vote_title.focus_set()

    def save():
        global cmd_recv
        send(f'start 3 vote {group_name} {vote_title.get()}')
        tmpi = 0
        while cmd_recv == '' and tmpi < 10:
            sleep(0.1)
            tmpi += 1
        if tmpi == 10:
            start_v.attributes('-topmost', False)
            msg.showerror('错误', '响应超时')
            start_v.attributes('-topmost', True)
            return
        recv = cmd_recv.split(' ')
        cmd_recv = ''
        if recv[0] == 'ok':
            start_v.attributes('-topmost', False)
            msg.showinfo('喜报', '成功发起投票')
            start_v.attributes('-topmost', True)
            start_v.destroy()
        else:
            start_v.attributes('-topmost', False)
            msg.showerror('错误', '无法发起投票：' + recv[1])
            start_v.attributes('-topmost', True)

    Button(start_v, text='确定', command=save).place(x=40, y=80, width=60, height=20)
    Button(start_v, text='取消', command=start_v.destroy).place(x=120, y=80, width=60, height=20)

    start_v.mainloop()


def vote():
    global cmd_recv
    send(f'get_title 1 {group_name}')
    tmpi = 0
    while cmd_recv == '' and tmpi < 10:
        sleep(0.1)
        tmpi += 1
    if tmpi == 10:
        msg.showerror('错误', '响应超时')
        return
    recv = cmd_recv.split(' ')
    cmd_recv = ''
    if recv[0] == 'ok':
        if msg.askyesno('投票', recv[1]):
            send(f'vote 2 {group_name} For')
        else:
            send(f'vote 2 {group_name} against')
        tmpi = 0
        while cmd_recv == '' and tmpi < 10:
            sleep(0.1)
            tmpi += 1
        if tmpi == 10:
            msg.showerror('错误', '响应超时')
            return
        recv = cmd_recv.split(' ')
        cmd_recv = ''
        if recv[0] == 'ok':
            msg.showinfo('喜报', '投票成功')
        else:
            msg.showerror('错误', '无法投票：'+recv[1])
    else:
        msg.showerror('错误', '无法投票：' + recv[1])


def get_result():
    global cmd_recv
    send(f'get_result 1 {group_name}')
    tmpi = 0
    while cmd_recv == '' and tmpi < 10:
        sleep(0.1)
        tmpi += 1
    if tmpi == 10:
        msg.showerror('错误', '响应超时')
        return
    recv = cmd_recv.split(' ')
    if recv[0] == 'info':
        msg.showinfo('结果', f'标题：{recv[1]}\n支持：{recv[2]}\n反对：{recv[3]}')
    else:
        msg.showerror('错误', '无法查看投票结果：'+recv[1])
    cmd_recv=''


def create_group():
    create_g = Tk()
    create_g.title('创建群聊')
    create_g.attributes('-topmost', True)
    create_g.focus_force()
    center(create_g)
    Label(create_g, text='群聊名称：').place(x=10, y=10)
    group_n = Entry(create_g)
    group_n.place(x=70, y=10, width=120)
    group_n.focus_set()
    Label(create_g, text='入群密码：').place(x=10, y=40)
    group_pwd = Entry(create_g)
    group_pwd.place(x=70, y=40, width=120)

    def save():
        global cmd_recv
        send(f'create 2 {group_n.get()} {group_pwd.get()}')
        tmpi = 0
        while cmd_recv == '' and tmpi < 10:
            sleep(0.1)
            tmpi += 1
        if tmpi == 10:
            create_g.attributes('-topmost', False)
            msg.showerror('错误', '响应超时')
            create_g.attributes('-topmost', True)
            return
        recv = cmd_recv.split(' ')
        cmd_recv = ''
        if recv[0] == 'ok':
            create_g.attributes('-topmost', False)
            msg.showinfo('喜报', '已成功创建群聊，可在菜单中手动进入群聊\n' + recv[1])
            create_g.attributes('-topmost', True)
            create_g.destroy()
        else:
            create_g.attributes('-topmost', False)
            msg.showerror('错误', '无法创建此群聊：' + recv[1])
            create_g.attributes('-topmost', True)

    Button(create_g, text='确定', command=save).place(x=40, y=80, width=60, height=20)
    Button(create_g, text='取消', command=create_g.destroy).place(x=120, y=80, width=60, height=20)

    create_g.mainloop()


def enter():
    enter_g = Tk()
    enter_g.title('进入群聊')
    enter_g.attributes('-topmost', True)
    enter_g.focus_force()
    center(enter_g)
    Label(enter_g, text='群聊名称：').place(x=10, y=10)
    group_n = Entry(enter_g)
    group_n.place(x=70, y=10, width=120)
    group_n.focus_set()

    def save():
        global cmd_recv, group_name
        send(f'enter 1 {group_n.get()}')
        tmpi = 0
        while cmd_recv == '' and tmpi < 10:
            sleep(0.1)
            tmpi += 1
        if tmpi == 10:
            enter_g.attributes('-topmost', False)
            msg.showerror('错误', '响应超时')
            enter_g.attributes('-topmost', True)
            return
        recv = cmd_recv.split(' ')
        cmd_recv = ''
        if recv[0] == 'ok':
            group_name = group_n.get()
            win.title(f'聊天窗口 - {usrname} in {group_name}')
            load()
            enter_g.attributes('-topmost', False)
            msg.showinfo('喜报', '已成功进入此群聊')
            enter_g.attributes('-topmost', True)
            enter_g.destroy()
        else:
            enter_g.attributes('-topmost', False)
            msg.showerror('错误', '无法进入此群聊：' + recv[1])
            enter_g.attributes('-topmost', True)

    Button(enter_g, text='确定', command=save).place(x=40, y=80, width=60, height=20)
    Button(enter_g, text='取消', command=enter_g.destroy).place(x=120, y=80, width=60, height=20)

    enter_g.mainloop()


def join():
    join_g = Tk()
    join_g.title('加入群聊')
    join_g.attributes('-topmost', True)
    join_g.focus_force()
    center(join_g)
    Label(join_g, text='群聊名称：').place(x=10, y=10)
    group_n = Entry(join_g)
    group_n.place(x=70, y=10, width=120)
    group_n.focus_set()
    Label(join_g, text='入群密码：').place(x=10, y=40)
    group_pwd = Entry(join_g)
    group_pwd.place(x=70, y=40, width=120)

    def save():
        global cmd_recv, group_name
        send(f'join 2 {group_n.get()} {group_pwd.get()}')
        tmpi = 0
        while cmd_recv == '' and tmpi < 10:
            sleep(0.1)
            tmpi += 1
        if tmpi == 10:
            join_g.attributes('-topmost', False)
            msg.showerror('错误', '响应超时')
            join_g.attributes('-topmost', True)
            return
        recv = cmd_recv.split(' ')
        cmd_recv = ''
        if recv[0] == 'ok':
            group_name = group_n.get()
            win.title(f'聊天窗口 - {usrname} in {group_name}')
            load()
            join_g.attributes('-topmost', False)
            msg.showinfo('喜报', '已成功加入此群聊，已自动进入')
            join_g.attributes('-topmost', True)
            join_g.destroy()
        else:
            join_g.attributes('-topmost', False)
            msg.showerror('错误', '无法加入此群聊：' + recv[1])
            join_g.attributes('-topmost', True)

    Button(join_g, text='确定', command=save).place(x=40, y=80, width=60, height=20)
    Button(join_g, text='取消', command=join_g.destroy).place(x=120, y=80, width=60, height=20)

    join_g.mainloop()


def get_group_info():
    global cmd_recv
    send(f'info 2 group {group_name}')
    tmpi = 0
    while cmd_recv == '' and tmpi < 10:
        sleep(0.1)
        tmpi += 1
    if tmpi == 10:
        msg.showerror('错误', '响应超时')
        return
    cmd = cmd_recv.split(' ')[0]
    if cmd == 'info':
        usr_info = to_dict(cmd_recv[5:])
        msg.showinfo('群聊信息', '\n'.join(f'{i}:{usr_info[i]},' for i in usr_info.keys()))
    else:
        msg.showerror('错误', '获取信息失败，请稍后重试')
    cmd_recv = ''


def withdraw():
    global cmd_recv, group_name
    send(f'withdraw 1 {group_name}')
    tmpi = 0
    while cmd_recv == '' and tmpi < 10:
        sleep(0.1)
        tmpi += 1
    if tmpi == 10:
        msg.showerror('错误', '响应超时')
        return
    recv = cmd_recv.split(' ')
    if recv[0] == 'ok':
        msg.showinfo('提示', f'已退出群聊{group_name}，自动进入公屏')
        group_name = 'public'
        win.title(f'聊天窗口 - {usrname} in public')
        load()
    else:
        msg.showerror('错误', recv[1])
    cmd_recv = ''


def launch_yi():
    system('start /d yi python yiLauncher.py')


menu = Menu(win)
win.config(menu=menu)
loc_settings_menu = Menu(menu, tearoff=0)
menu.add_cascade(label='本地设置', menu=loc_settings_menu)
loc_settings_menu.add_command(label='检查更新', command=check)
loc_settings_menu.add_command(label='本地设置', command=local_setting)

usr_settings_menu = Menu(menu, tearoff=0)
menu.add_cascade(label='用户设置', menu=usr_settings_menu)
usr_settings_menu.add_command(label='更改用户名', command=modify_name)
usr_settings_menu.add_command(label='更改密码', command=modify_password)
usr_settings_menu.add_command(label='查看用户信息', command=get_user_info)
usr_settings_menu.add_command(label='注销账号', command=cancel)
usr_settings_menu.add_separator()
remember_me = BooleanVar()
remember_me.set(usr_settings['remember_me'])
usr_settings_menu.add_checkbutton(label='记住密码', command=set_remember_me, variable=remember_me)
show_uid = BooleanVar()
show_uid.set(usr_settings['show_uid'])
usr_settings_menu.add_checkbutton(label='在聊天框中展示发送者的uid', command=set_show_uid, variable=show_uid)

grp_menu = Menu(menu, tearoff=0)
menu.add_cascade(label='群聊', menu=grp_menu)
grp_menu.add_command(label='发起投票', command=start_vote)
grp_menu.add_command(label='投票',command=vote)
grp_menu.add_command(label='查看投票结果', command=get_result)
grp_menu.add_command(label='查看群聊信息', command=get_group_info)
grp_menu.add_command(label='退出群聊', command=withdraw)
grp_menu.add_separator()
grp_menu.add_command(label='创建群聊', command=create_group)
grp_menu.add_command(label='进入群聊', command=enter)
grp_menu.add_command(label='加入群聊', command=join)

game_menu = Menu(menu, tearoff=0)
menu.add_cascade(label='游戏', menu=game_menu)
game_menu.add_command(label='贪吃易', command=launch_yi)

bt1 = Button(win, text='发送')
bt1['command'] = send_message

recv_msg.place(x=5, y=5)
send_msg.place(x=5, y=540)
ys2.place(x=475, y=5, height=535)
ys1.place(x=430, y=540, height=55)
bt1.place(x=450, y=540, width=45, height=55)

win.mainloop()

client_socket.close()
