import json
from socket import socket
import sys
import os
from typing import Union

sys.path.append(os.path.abspath(os.path.join(__file__, '..', '..')))
from common.errors import IncorrectPort
from log.log_utils import log


@log
def send_message(s: socket, message: dict):
    if not isinstance(message, dict):
        raise ValueError('message must be dict')
    message_str = json.dumps(message)
    return s.send(message_str.encode('utf-8'))


def receive_message(s: socket):
    message = s.recv(1000)
    return json.loads(message.decode('utf-8'))


def check_port(port: Union[str, int]):
    if isinstance(port, str) and port.isdigit() and 1024 <= int(port) <= 65535:
        return int(port)
    if isinstance(port, int) and 1024 <= int(port) <= 65535:
        return port
    raise IncorrectPort('')


def get_message(message: dict):
    return f'got message {json.dumps(message, indent=4)}'
