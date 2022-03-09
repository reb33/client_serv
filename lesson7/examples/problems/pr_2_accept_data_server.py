""" Программа сервера для получения приветствия от клиента и отправки ответа """

from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR

SERV_SOCK = socket(AF_INET, SOCK_STREAM)
SERV_SOCK.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
SERV_SOCK.bind(('', 8007))
SERV_SOCK.listen(1)
SOCKETS = []

try:
    while True:
        CLIENT_S, ADDR = SERV_SOCK.accept()
        SOCKETS.append(CLIENT_S)
        for CLIENT_SOCK in SOCKETS:
            DATA = CLIENT_SOCK.recv(4096)
            if DATA == b'exit':
                # find CLIENT_SOCK and remove from DATA
                SOCKETS.remove(CLIENT_SOCK)
                CLIENT_SOCK.close()
            print(f"Сообщение: {DATA.decode('utf-8')} было отправлено клиентом: {ADDR})")
            MSG = 'Привет, клиент'
            CLIENT_SOCK.send(MSG.encode('utf-8'))
finally:
    SERV_SOCK.close()
