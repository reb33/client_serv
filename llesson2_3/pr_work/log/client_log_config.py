import logging
import os.path

LOG = logging.getLogger('client')

file_path = os.path.join(os.path.abspath(__file__), '..', "client.log")
FILE_HANDLER = logging.FileHandler(file_path, encoding='utf-8')
FILE_HANDLER.setLevel(logging.DEBUG)
STREAM_HANDLER = logging.StreamHandler()
STREAM_HANDLER.setLevel(logging.INFO)

FORMATTER = logging.Formatter("%(asctime)s %(levelname)s %(module)s %(message)s ")

FILE_HANDLER.setFormatter(FORMATTER)
STREAM_HANDLER.setFormatter(FORMATTER)


LOG.addHandler(FILE_HANDLER)
LOG.addHandler(STREAM_HANDLER)
LOG.setLevel(logging.DEBUG)

if __name__ == '__main__':
    LOG.info('check')
