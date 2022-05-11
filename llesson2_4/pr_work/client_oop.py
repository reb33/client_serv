import argparse
import configparser
import threading
import time
from contextlib import contextmanager
from datetime import datetime

from common.errors import IncorrectDataRecivedError, ServerError, ReqFieldMissingError
from common.utils import *
from common.variables import *
from client_db import ClientDB
from log.log_utils import log
from meta import ClientVerifier

# Инициализация клиентского логера
logger = logging.getLogger('client')


class ClientSender(metaclass=ClientVerifier):

    def __init__(self, sock, account_name) -> None:
        self.sock = sock
        self.account_name = account_name
        self.client_db = ClientDB(account_name)

    def create_exit_message(self):
        return {
            ACTION: EXIT,
            TIME: time.time(),
            ACCOUNT_NAME: self.account_name
        }

    def _send_message(self, message_dict):
        try:
            return send_message(self.sock, message_dict)
        except:
            logger.critical('Потеряно соединение с сервером.')
            exit(1)

    def get_contracts(self):
        message_dict = {
            ACTION: GET_CONTACTS,
            SENDER: self.account_name,
            TIME: time.time(),
        }
        self._send_message(message_dict)
        resp = receive_message(self.sock)
        if resp[RESPONSE] == '200':
            return resp[CONTACTS]

    def add_contract(self):
        contact = input('введите кого добавить')
        message_dict = {
            ACTION: ADD_CONTACT,
            SENDER: self.account_name,
            TIME: time.time(),
            CONTACT: contact
        }
        self._send_message(message_dict)
        resp = receive_message(self.sock)
        if resp.get(RESPONSE) == '200':
            logger.info('контакт добавлен')
            self.client_db.add_contact(contact)
        else:
            raise ServerError('Ошибка создания контакта')

    def del_contract(self):
        contact = input('введите кого удалить')
        message_dict = {
            ACTION: DEL_CONTACT,
            SENDER: self.account_name,
            TIME: time.time(),
            CONTACT: contact
        }
        self._send_message(message_dict)
        resp = receive_message(self.sock)
        if resp.get(RESPONSE) == '200':
            logger.info('контакт удален')
            self.client_db.del_contact(contact)
        else:
            raise ServerError('Ошибка удаление контакта')

    def sender_message(self):
        while True:
            command = input('введите команду s-отправить, e-выход, c-управление списком контактов\n')
            if command.strip() == 'e':
                send_message(self.sock, self.create_exit_message())
                return
            if command.strip() == 's':
                to = input('отправить сообщение кому: ')
                mess = input('введите сообщение: ')
                message_dict = {
                    ACTION: MESSAGE,
                    SENDER: self.account_name,
                    DESTINATION: to,
                    TIME: time.time(),
                    MESSAGE_TEXT: mess
                }
                logger.debug(f'Сформирован словарь сообщения: {message_dict}')
                self._send_message(message_dict)
                logger.info(f'Отправлено сообщение для пользователя {to}')
                self.client_db.add_message(self.account_name, to, mess, datetime.fromtimestamp(message_dict[TIME]))

            if command.strip() == 'c':
                next_command = input('g-получить список контактов, a-добавить контакт, d-удалить контакт\n')
                if next_command.strip() == 'g':
                    logger.info(f'контакты {self.get_contracts()}')
                if next_command.strip() == 'a':
                    self.add_contract()
                if next_command.strip() == 'd':
                    self.del_contract()


class ClientReader(threading.Thread, metaclass=ClientVerifier):
    def __init__(self, sock, account_name):
        self.account_name = account_name
        self.sock = sock
        self.client_db = ClientDB(account_name)
        super().__init__()

    # Основной цикл приёмника сообщений, принимает сообщения, выводит в консоль. Завершается при потере соединения.
    def run(self):
        while True:
            try:
                message = receive_message(self.sock)
                if ACTION in message and message[ACTION] == MESSAGE and SENDER in message and DESTINATION in message \
                        and MESSAGE_TEXT in message and message[DESTINATION] == self.account_name:
                    print(f'\nПолучено сообщение от пользователя {message[SENDER]}:\n{message[MESSAGE_TEXT]}')
                    logger.info(f'Получено сообщение от пользователя {message[SENDER]}:\n{message[MESSAGE_TEXT]}')
                    self.client_db.add_message(
                        message[SENDER],
                        self.account_name,
                        message[MESSAGE_TEXT],
                        datetime.fromtimestamp(message[TIME])
                    )
                else:
                    logger.error(f'Получено некорректное сообщение с сервера: {message}')
            except IncorrectDataRecivedError:
                logger.error(f'Не удалось декодировать полученное сообщение.')
            except (OSError, ConnectionError, ConnectionAbortedError, ConnectionResetError, json.JSONDecodeError):
                logger.critical(f'Потеряно соединение с сервером.')
                break


# Функция генерирует запрос о присутствии клиента
@log
def create_presence(account_name):
    out = {
        ACTION: PRESENCE,
        TIME: time.time(),
        USER: {
            ACCOUNT_NAME: account_name
        }
    }
    logger.debug(f'Сформировано {PRESENCE} сообщение для пользователя {account_name}')
    return out


# Функция разбирает ответ сервера на сообщение о присутствии, возращает 200 если все ОК или генерирует исключение при\
# ошибке.
@log
def process_response_ans(message):
    logger.debug(f'Разбор приветственного сообщения от сервера: {message}')
    if RESPONSE in message:
        if message[RESPONSE] == 200:
            return '200 : OK'
        elif message[RESPONSE] == 400:
            raise ServerError(f'400 : {message[ERROR]}')
    raise ReqFieldMissingError(RESPONSE)


@contextmanager
def get_client_socket():
    config = configparser.ConfigParser()

    dir_path = os.path.dirname(os.path.realpath(__file__))
    config.read(f"{dir_path}/{'server.ini'}")
    parser = argparse.ArgumentParser()
    parser.add_argument('addr', default=DEFAULT_IP_ADDRESS, nargs='?')
    parser.add_argument('port', default=config['SETTINGS']['default_port'], type=int, nargs='?')
    parser.add_argument('-n', '--name', default=None, nargs='?')
    namespace = parser.parse_args(sys.argv[1:])
    server_address = namespace.addr
    server_port = check_port(namespace.port)
    client_name = namespace.name
    if not client_name:
        client_name = input('Введите имя пользователя: ')

    socket_client = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
    try:
        socket_client.connect((server_address, server_port))
        logger.info(
            f'Запущен клиент с парамертами: адрес сервера: {server_address} , '
            f'порт: {server_port}, имя пользователя: {client_name}')
        yield socket_client, client_name
    except ServerError as error:
        logger.error(f'При установке соединения сервер вернул ошибку: {error.text}')
        exit(1)
    except (ConnectionRefusedError, ConnectionError):
        logger.critical(
            f'Не удалось подключиться к серверу {server_address}:{server_port}, '
            f'конечный компьютер отверг запрос на подключение.')
        exit(1)
    finally:
        socket_client.close()


def main():
    # Сообщаем о запуске

    with get_client_socket() as (socket_client, client_name):
        # Инициализация сокета и сообщение серверу о нашем появлении
        try:
            send_message(socket_client, create_presence(client_name))
            answer = process_response_ans(receive_message(socket_client))
            logger.info(f'Установлено соединение с сервером. Ответ сервера: {answer}')
        except json.JSONDecodeError:
            logger.error('Не удалось декодировать полученную Json строку.')
            exit(1)
        except ReqFieldMissingError as missing_error:
            logger.error(f'В ответе сервера отсутствует необходимое поле {missing_error.missing_field}')
            exit(1)

        else:
            # Если соединение с сервером установлено корректно, запускаем клиентский процесс приёма сообщений
            module_reciver = ClientReader(socket_client, client_name)
            module_reciver.daemon = True
            module_reciver.start()

            # затем запускаем отправку сообщений и взаимодействие с пользователем.
            ClientSender(socket_client, client_name).sender_message()


if __name__ == '__main__':
    main()
