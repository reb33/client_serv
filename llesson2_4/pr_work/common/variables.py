# Порт поумолчанию для сетевого ваимодействия
import logging

# IP адрес по умолчанию для подключения клиента
DEFAULT_IP_ADDRESS = '127.0.0.1'
# Максимальная очередь подключений
MAX_CONNECTIONS = 5
# Максимальная длинна сообщения в байтах
MAX_PACKAGE_LENGTH = 1024
# Кодировка проекта
ENCODING = 'utf-8'
# Текущий уровень логирования
LOGGING_LEVEL = logging.DEBUG

# Прококол JIM основные ключи:
ACTION = 'action'
TIME = 'time'
USER = 'user'
ACCOUNT_NAME = 'account_name'
SENDER = 'from'
DESTINATION = 'to'

# Прочие ключи, используемые в протоколе
PRESENCE = 'presence'
RESPONSE = 'response'
ERROR = 'error'
MESSAGE = 'message'
GET_CONTACTS = 'get_contacts'
ADD_CONTACT = 'add_contact'
DEL_CONTACT = 'del_contact'
CONTACT = 'contact'
CONTACTS = 'contacts'

MESSAGE_TEXT = 'mess_text'
EXIT = 'exit'

# Словари - ответы:
# 200
RESPONSE_200 = {RESPONSE: 200}
# 400
RESPONSE_400 = {
            RESPONSE: 400,
            ERROR: None
        }