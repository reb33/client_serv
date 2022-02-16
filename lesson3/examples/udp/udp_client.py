"""Программа клиента, передающего серверу сообщения при каждом запросе на соединение"""

from socket import socket, AF_INET, SOCK_DGRAM, SOL_SOCKET, SO_BROADCAST

CLIENT_SOCK = socket(AF_INET, SOCK_DGRAM)
CLIENT_SOCK.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)

try:
    while True:
        MES = 'Привет, сервер'
        CLIENT_SOCK.sendto(MES.encode('utf-8'), ('localhost', 8888))
        MSG, ADDR = CLIENT_SOCK.recvfrom(1024)
        print(MSG.decode('utf-8'))
finally:
    CLIENT_SOCK.close()
