import json
from socket import socket


def send_message(s: socket, message: dict):
    if not isinstance(message, dict):
        raise ValueError('message must be dict')
    message_str = json.dumps(message)
    return s.send(message_str.encode('utf-8'))


def receive_message(s: socket):
    message = s.recv(1000)
    return json.loads(message.decode('utf-8'))


def check_port(port: str):
    if port.isdigit() and 1024 <= int(port) <= 65535:
        return int(port)
    raise ValueError('указан некорректный порт')


def print_message(message: dict):
    print(f'got message {json.dumps(message, indent=4)}')
