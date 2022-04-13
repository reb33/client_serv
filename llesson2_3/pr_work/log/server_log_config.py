import logging.handlers
import os.path

LOG = logging.getLogger('server')

file_path = os.path.join(os.path.abspath(__file__), '..', "server.log")
FILE_HANDLER = logging.handlers.TimedRotatingFileHandler(file_path, encoding='utf-8', when='d')
FILE_HANDLER.setLevel(logging.DEBUG)

FORMATTER = logging.Formatter("%(asctime)s %(levelname)s %(module)s %(message)s ")

FILE_HANDLER.setFormatter(FORMATTER)

LOG.addHandler(FILE_HANDLER)
LOG.setLevel(logging.DEBUG)

if __name__ == '__main__':
    LOG.info('check')
