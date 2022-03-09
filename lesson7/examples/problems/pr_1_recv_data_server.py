""" Программа сервера для получения приветствия от клиента и отправки ответа """

from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR

SERV_SOCK = socket(AF_INET, SOCK_STREAM)
SERV_SOCK.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
SERV_SOCK.bind(('', 8007))
SERV_SOCK.listen()

try:
    while True:
        CLIENT_SOCK, ADDR = SERV_SOCK.accept()
        DATA = CLIENT_SOCK.recv(4096)
        print(f"Сообщение: {DATA.decode('utf-8')} было отправлено клиентом: {ADDR})")
        MSG = 'Привет, клиент'
        CLIENT_SOCK.send(MSG.encode('utf-8'))
        CLIENT_SOCK.close()
finally:
    SERV_SOCK.close()
