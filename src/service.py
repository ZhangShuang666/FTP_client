import socket
from config import settings


def execute(conn):
    pass


def main():
    ip_port = (settings.server, settings.port)
    conn = socket.socket()
    conn.connect(ip_port)
    welcome_bytes = conn.recv(1024)
    print(welcome_bytes.decode(encoding='utf-8'))
    execute(conn)
    conn.close()



