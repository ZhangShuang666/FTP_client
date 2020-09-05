import socket
import os
import re
import json
from config import settings
from lib import common


def help_info():
    print("""
            cmd|命令
            post|文件路径
            get|下载文件路径
            exit|退出
    """)


def login(conn):
    print("login")
    while True:
        username = input("请输入用户名：")
        password = input("请输入密码：")
        login_info = {
            'username': username,
            'password': password
        }
        conn.sendall(json.dumps(login_info).encode(encoding='utf-8'))

        if conn.recv(1024).decode(encoding='utf-8') == '4002':
            print("授权成功")
            break
        else:
            print("用户名或者密码错误")


def get(conn, inp):
    print("get")
    pass


def post(conn, inp):
    method, file_path = inp.split('|', 1)
    local_path, target_path = re.split('\s+', file_path, 1)
    file_size_byte = os.stat(local_path).st_size
    file_name = os.path.basename(local_path)
    file_md5 = common.fetch_file_md5(local_path)
    post_info = "post|%s|%s|%s|%s" % (file_size_byte, file_name, file_md5, target_path)
    conn.sendall(post_info.encode(encoding='utf-8'))

    result_exist = conn.recv(1024).decode(encoding='utf-8')
    print(result_exist)
    if result_exist == '4001':
        login(conn)
        return

    has_sent = 0
    if result_exist == '2003':
        inp = input("文件已经存在，是否续传：Y/N：")
        if inp == 'Y':
            conn.sendall('2004'.encode(encoding='utf-8'))
            result_continue_pos = conn.recv(1024).decode(encoding='utf-8')
            has_sent = int(result_continue_pos)
        else:
            conn.sendall('2005'.encode(encoding='utf-8'))
    file_obj = open(local_path, 'rb')
    file_obj.seek(has_sent)

    while file_size_byte > has_sent:
        data = file_obj.read(1024)
        conn.sendall(data)
        has_sent += len(data)
        common.bar(has_sent, file_size_byte)
    file_obj.close()
    print("上传成功")


def cmd(conn, inp):
    print("cmd")
    pass


def execute(conn):
    choice_dict = {
        'cmd': cmd,
        'get': get,
        'post': post,
    }
    help_info()
    while True:
        inp = input("请输入选项：")
        if inp == help:
            help_info()
        choice = inp.split('|', 1)[0]
        if choice == "exit":
            return
        if choice in choice_dict:
            func = choice_dict[choice]
            func(conn, inp)


def main():
    ip_port = (settings.server, settings.port)
    conn = socket.socket()
    conn.connect(ip_port)
    welcome_bytes = conn.recv(1024)
    print(welcome_bytes.decode(encoding='utf-8'))
    execute(conn)
    conn.close()
