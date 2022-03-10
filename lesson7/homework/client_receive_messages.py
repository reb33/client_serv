import logging
from contextlib import contextmanager
from socket import socket, AF_INET, SOCK_STREAM
from sys import argv
from time import sleep

from common.errors import IncorrectPort
from common.utils import check_port, receive_message
from common.variables import DEFAULT_PORT, DEFAULT_API_ADDRESS
import log.client_log_config

CLIENT_LOG = logging.getLogger('client')


@contextmanager
def get_client_socket():
    addr = argv[1] if len(argv) > 2 else DEFAULT_API_ADDRESS
    try:
        port = check_port(argv[2]) if len(argv) > 2 else DEFAULT_PORT
    except IncorrectPort as e:
        CLIENT_LOG.error(str(e))
        raise e

    socket_client = socket(family=AF_INET, type=SOCK_STREAM)
    try:
        socket_client.connect((addr, port))
        yield socket_client
    except ConnectionRefusedError:
        CLIENT_LOG.error('не удалось подключиться')
        raise
    finally:
        socket_client.close()


def main():
    with get_client_socket() as socket_client:
        while True:
            message = receive_message(socket_client)
            CLIENT_LOG.info(message['message'])


if __name__ == '__main__':
    main()
