import json
import socket
import sys
import os
from json import JSONDecodeError
from typing import Union


sys.path.append(os.path.abspath(os.path.join(__file__, '..', '..')))
from common.errors import IncorrectPort, IncorrectDataRecivedError
from log.log_utils import log
from common.variables import MAX_PACKAGE_LENGTH, ENCODING


@log
def send_message(s: socket.socket, message: dict):
    if not isinstance(message, dict):
        raise ValueError('message must be dict')
    message_str = json.dumps(message)
    return s.send(message_str.encode('utf-8'))


def receive_message(s: socket.socket):
    encoded_response = s.recv(MAX_PACKAGE_LENGTH)
    if isinstance(encoded_response, bytes):
        json_response = encoded_response.decode(ENCODING)
        try:
            response = json.loads(json_response)
            return response
        except JSONDecodeError:
            raise IncorrectDataRecivedError
    else:
        raise IncorrectDataRecivedError


def check_port(port: Union[str, int]):
    if isinstance(port, str) and port.isdigit() and 1024 <= int(port) <= 65535:
        return int(port)
    if isinstance(port, int) and 1024 <= int(port) <= 65535:
        return port
    raise IncorrectPort('')

