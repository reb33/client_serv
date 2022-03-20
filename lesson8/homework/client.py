import argparse
import logging
from contextlib import contextmanager
from datetime import datetime
from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread

from common.errors import IncorrectPort, IncorrectResponseFromServer
from common.utils import check_port, receive_message, send_message
from common.variables import DEFAULT_PORT, DEFAULT_API_ADDRESS

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


def receiver_message(socket_, client_name):
    while True:
        message = receive_message(socket_)
        # print(message)
        if message['recr'] == client_name:
            print(f'получено сообщение: {message}')


def sender_message(socket_):
    while True:
        command = input('введите команду s-отправить, e-выход:\n')
        if command.strip() == 'e':
            return
        if command.strip() == 's':
            recr_client = input('отправить сообщение кому: ')
            mess = input('введите сообщение: ')
            send_message(socket_, {
                'recr': recr_client,
                'mess': mess
            })


@contextmanager
def get_client_socket():
    parser = argparse.ArgumentParser()
    parser.add_argument('--addr', default=DEFAULT_API_ADDRESS)
    parser.add_argument('--port', type=int, default=DEFAULT_PORT)
    parser.add_argument('-n', '--name', default='client1')
    args = parser.parse_args()
    print(f'клиент {args.name}')
    try:
        port = check_port(args.port)
    except IncorrectPort as e:
        CLIENT_LOG.error(str(e))
        raise e

    socket_client = socket(family=AF_INET, type=SOCK_STREAM)
    try:
        socket_client.connect((args.addr, port))
        yield socket_client, args.name
    except ConnectionRefusedError:
        CLIENT_LOG.error('не удалось подключиться')
        raise
    finally:
        socket_client.close()


def main():
    with get_client_socket() as (socket_client, client_name):
        Thread(target=receiver_message, args=(socket_client, client_name), daemon=True).start()
        sender_message(socket_client)


if __name__ == '__main__':
    main()
