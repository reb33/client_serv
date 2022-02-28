# Реализовать простое клиент-серверное взаимодействие по протоколу JIM (JSON instant messaging):
# клиент отправляет запрос серверу; сервер отвечает соответствующим кодом результата.
# Клиент и сервер должны быть реализованы в виде отдельных скриптов, содержащих соответствующие функции.
# Функции клиента: сформировать presence-сообщение; отправить сообщение серверу;
# получить ответ сервера; разобрать сообщение сервера;
# параметры командной строки скрипта client.py []:
# addr — ip-адрес сервера; port — tcp-порт на сервере, по умолчанию 7777.
from datetime import datetime
from socket import socket, AF_INET, SOCK_STREAM
from sys import argv
import logging
import log.client_log_config

from common.utils import check_port, receive_message, send_message, get_message
from common.variables import DEFAULT_PORT, DEFAULT_API_ADDRESS
from common.errors import IncorrectPort, IncorrectResponseFromServer

CLIENT_LOG = logging.getLogger('client')


def gen_presence_message(account):
    return {
        "action": "authenticate",
        "time": datetime.now().timestamp(),
        "user": {
            "account_name": f"{account}",
            "password": "CorrectHorseBatterStaple"
        }
    }


def check_response(message, expected_status):
    if message.get('response') == expected_status:
        return message
    CLIENT_LOG.error(f'server response {message}')
    raise IncorrectResponseFromServer()


def main():
    addr = argv[1] if len(argv) > 2 else DEFAULT_API_ADDRESS
    try:
        port = check_port(argv[2]) if len(argv) > 2 else DEFAULT_PORT
    except IncorrectPort as e:
        CLIENT_LOG.error(str(e))
        raise e

    socket_client = socket(family=AF_INET, type=SOCK_STREAM)
    try:
        socket_client.connect((addr, port))
    except ConnectionRefusedError:
        CLIENT_LOG.error('не удалось подключиться')
        raise
    send_message(socket_client, gen_presence_message('Vasya'))
    message = receive_message(socket_client)
    CLIENT_LOG.info(get_message(message))
    check_response(message, 200)
    socket_client.close()


if __name__ == '__main__':
    main()
