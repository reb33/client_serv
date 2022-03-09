""" Программа сервера для отправки приветствия сервера и получения ответа """

from socket import socket, AF_INET, SOCK_STREAM

CLIENT_SOCK = socket(AF_INET, SOCK_STREAM)
CLIENT_SOCK.connect(('localhost', 8007))
while True:
    MSG = 'Привет, сервер'
    CLIENT_SOCK.send(MSG.encode('utf-8'))
    DATA = CLIENT_SOCK.recv(4096)
    print(f"Сообщение от сервера: {DATA.decode('utf-8')} длиной {len(DATA)} байт")
CLIENT_SOCK.close()
