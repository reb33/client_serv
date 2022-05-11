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
        name_log = 'client' if 'client.py' in sys.argv[0] else 'server'
        LOGGER = logging.getLogger(name_log)

        stack = inspect.stack()
        arguments = ', '.join(list(map(str, args))+[f'{k}={v}' for k, v in kwargs.items()])
        message = f'функция {func.__name__}({arguments}) вызвана из функции {stack[1].function} '
        LOGGER.info(message)

        return func(*args, **kwargs)
    return inner
