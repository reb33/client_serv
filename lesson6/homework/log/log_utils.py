import inspect
import logging
import sys
import os
from functools import wraps
sys.path.append(os.path.abspath(os.path.join(__file__, '..', '..')))
import log.client_log_config
import log.server_log_config


CLIENT_LOG = logging.getLogger('client')
SERVER_LOG = logging.getLogger('server')

def log(func):
    @wraps(func)
    def inner(*args, **kwargs):
        is_client = False
        is_server = False
        if 'client.py' in sys.argv[0]:
            is_client = True
        if 'server.py' in sys.argv[0]:
            is_server = True

        stack = inspect.stack()
        arguments = ', '.join(list(map(str, args))+[f'{k}={v}' for k, v in kwargs.items()])
        message = f'функция {func.__name__}({arguments}) вызвана из функции {stack[1].function} '
        print_log(is_client, is_server, message)

        return func(*args, **kwargs)
    return inner


def print_log(is_client, is_server, message):
    if is_client:
        CLIENT_LOG.info(message)
    if is_server:
        SERVER_LOG.info(message)
