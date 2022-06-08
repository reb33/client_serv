import configparser
import socket
import argparse
import logging
import select
import threading
from datetime import datetime

from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import QApplication, QMessageBox

import log.server_log_config
from common.variables import *
from common.utils import *
from common.errors import IncorrectPort
from server_gui import MainWindow, gui_create_model, HistoryWindow, create_stat_model, ConfigWindow
from server_db import ServerDB
from meta import ServerVerifier
from log.log_utils import log

# Инициализация логирования сервера.
logger = logging.getLogger('server')
new_connection = False
conflag_lock = threading.Lock()


# Парсер аргументов командной строки.
@log
def arg_parser(default_port):
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', default=default_port, type=int, nargs='?')
    parser.add_argument('-a', default='', nargs='?')
    namespace = parser.parse_args(sys.argv[1:])
    listen_address = namespace.a
    listen_port = namespace.p
    return listen_address, listen_port


class Port:

    def __set_name__(self, owner, name):
        self.name = name

    def __set__(self, instance, value):
        if isinstance(value, str) and value.isdigit():
            value = int(value)
        if isinstance(value, int) and 1024 <= int(value) <= 65535:
            instance.__dict__[self.name] = value
            return
        raise IncorrectPort('')

    def __get__(self, instance, owner):
        return instance.__dict__[self.name]


# Основной класс сервера
class Server(threading.Thread, metaclass=ServerVerifier):
    port = Port()

    def __init__(self, listen_address, listen_port, db):
        # Параметры подключения
        self.addr = listen_address
        self.port = listen_port

        # Список подключённых клиентов.
        self.clients = []

        # Список сообщений на отправку.
        self.messages = []

        # Словарь содержащий сопоставленные имена и соответствующие им сокеты.
        self.names = dict()

        self.db = db
        super().__init__()

    def init_socket(self):
        logger.info(
            f'Запущен сервер, порт для подключений: {self.port}, '
            f'адрес с которого принимаются подключения: {self.addr}. '
            f'Если адрес не указан, принимаются соединения с любых адресов.')
        # Готовим сокет
        transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        transport.bind((self.addr, self.port))
        transport.settimeout(0.5)

        # Начинаем слушать сокет.
        self.sock = transport
        self.sock.listen()

    def run(self):
        # Инициализация Сокета
        self.init_socket()

        # Основной цикл программы сервера
        while True:
            # Ждём подключения, если таймаут вышел, ловим исключение.
            try:
                client, client_address = self.sock.accept()
            except OSError:
                pass
            else:
                logger.info(f'Установлено соедение с ПК {client_address}')
                self.clients.append(client)

            recv_data_lst = []
            send_data_lst = []
            err_lst = []
            # Проверяем на наличие ждущих клиентов
            try:
                if self.clients:
                    recv_data_lst, send_data_lst, err_lst = select.select(self.clients, self.clients, [], 0)
            except OSError:
                pass

            # принимаем сообщения и если ошибка, исключаем клиента.
            if recv_data_lst:
                for client_with_message in recv_data_lst:
                    try:
                        self.process_client_message(receive_message(client_with_message), client_with_message)
                    except Exception as e:
                        logger.info(f'Клиент {client_with_message.getpeername()} отключился от сервера.')
                        self.clients.remove(client_with_message)

            # Если есть сообщения, обрабатываем каждое.
            for message in self.messages:
                try:
                    self.process_message(*message, listen_socks=send_data_lst)
                except Exception as e:
                    logger.info(f'Связь с клиентом с именем '
                                f'{message[DESTINATION]} была потеряна, '
                                f' ошибка {e}')
                    self.clients.remove(self.names[message[DESTINATION]])
                    self.db.logout_client(message[DESTINATION])
                    with conflag_lock:
                        global new_connection
                        new_connection = True
                    del self.names[message[DESTINATION]]
            self.messages.clear()

    def get_login_by_socket(self, looked_client):
        for name, client in self.names.items():
            if client.getpeername() == looked_client.getpeername():
                return name

    # Функция адресной отправки сообщения определённому клиенту.
    # Принимает словарь сообщение, список зарегистрированных
    # пользователей и слушающие сокеты. Ничего не возвращает.
    def process_message(self, sender, message, listen_socks):
        if message[DESTINATION] in self.names and \
                self.names[message[DESTINATION]] in listen_socks:
            send_message(self.names[message[DESTINATION]], message)
            self.db.add_message(self.get_login_by_socket(sender), message[DESTINATION])
            logger.info(f'Отправлено сообщение пользователю {message[DESTINATION]} '
                        f'от пользователя {message[SENDER]}.')
        elif message[DESTINATION] in self.names \
                and self.names[message[DESTINATION]] not in listen_socks:
            raise ConnectionError
        else:
            logger.error(
                f'Пользователь {message[DESTINATION]} не зарегистрирован '
                f'на сервере, отправка сообщения невозможна.')

    # Обработчик сообщений от клиентов, принимает словарь - сообщение от клиента,
    # проверяет корректность, отправляет словарь-ответ в случае необходимости.
    def process_client_message(self, message, client):
        global new_connection
        logger.debug(f'Разбор сообщения от клиента : {message}')
        # Если это сообщение о присутствии, принимаем и отвечаем
        if ACTION in message and message[ACTION] == PRESENCE \
                and TIME in message and USER in message:
            # Если такой пользователь ещё не зарегистрирован, регистрируем,
            # иначе отправляем ответ и завершаем соединение.
            if message[USER][ACCOUNT_NAME] not in self.names.keys():

                self.db.login_client(message[USER][ACCOUNT_NAME], client, datetime.fromtimestamp(message[TIME]))
                self.names[message[USER][ACCOUNT_NAME]] = client
                send_message(client, RESPONSE_200)
                with conflag_lock:
                    new_connection = True
            else:
                response = RESPONSE_400
                response[ERROR] = 'Имя пользователя уже занято.'
                send_message(client, response)
                self.clients.remove(client)
                client.close()
            return
        # Если это сообщение, то добавляем его в очередь сообщений. Ответ не требуется.
        elif ACTION in message \
                and message[ACTION] == MESSAGE \
                and DESTINATION in message \
                and TIME in message \
                and SENDER in message \
                and MESSAGE_TEXT in message:
            self.messages.append((client, message))
            return
        # Если клиент выходит
        elif ACTION in message \
                and message[ACTION] == EXIT \
                and ACCOUNT_NAME in message:
            self.clients.remove(self.names[message[ACCOUNT_NAME]])
            self.names[message[ACCOUNT_NAME]].close()
            self.db.logout_client(message[ACCOUNT_NAME])
            del self.names[message[ACCOUNT_NAME]]
            with conflag_lock:
                new_connection = True
            return
        elif ACTION in message \
                and message[ACTION] == ADD_CONTACT \
                and TIME in message \
                and SENDER in message \
                and CONTACT in message:
            self.db.save_contact(message[SENDER], message[CONTACT])
        elif ACTION in message \
                and message[ACTION] == DEL_CONTACT \
                and TIME in message \
                and SENDER in message \
                and CONTACT in message:
            self.db.del_contact(message[SENDER], message[CONTACT])
        elif ACTION in message \
                and message[ACTION] == GET_CONTACTS \
                and TIME in message \
                and CONTACT in message:
            self.db.get_contracts(message[SENDER])
        # Иначе отдаём Bad request
        else:
            response = RESPONSE_400
            response[ERROR] = 'Запрос некорректен.'
            send_message(client, response)
            return


def main():
    # Загрузка параметров командной строки, если нет параметров,
    # то задаём значения по умолчанию.
    config = configparser.ConfigParser()

    dir_path = os.path.dirname(os.path.realpath(__file__))
    config.read(f"{dir_path}/{'server.ini'}")
    listen_address, listen_port = arg_parser(config['SETTINGS']['default_port'])

    # Создание экземпляра класса - сервера.
    db = ServerDB(config['SETTINGS']['Database_file'])
    db.clear_active_users()
    server = Server(listen_address, listen_port, db)
    server.daemon = True
    server.start()

    app = QApplication(sys.argv)
    main_window = MainWindow()

    main_window.statusBar().showMessage('Server working')
    main_window.active_clients_table.setModel(gui_create_model(db))
    main_window.active_clients_table.resizeColumnsToContents()
    main_window.active_clients_table.resizeRowsToContents()

    # Функция, обновляющая список подключённых, проверяет флаг подключения, и
    # если надо обновляет список
    def list_update():
        global new_connection
        if new_connection:
            main_window.active_clients_table.setModel(
                gui_create_model(db))
            main_window.active_clients_table.resizeColumnsToContents()
            main_window.active_clients_table.resizeRowsToContents()
            with conflag_lock:
                new_connection = False

    # Функция, создающая окно со статистикой клиентов
    def show_statistics():
        global stat_window
        stat_window = HistoryWindow()
        stat_window.history_table.setModel(create_stat_model(db))
        stat_window.history_table.resizeColumnsToContents()
        stat_window.history_table.resizeRowsToContents()
        stat_window.show()

    # Функция создающяя окно с настройками сервера.
    def server_config():
        global config_window
        # Создаём окно и заносим в него текущие параметры
        config_window = ConfigWindow()
        config_window.db_path.insert(config['SETTINGS']['Database_path'])
        config_window.db_file.insert(config['SETTINGS']['Database_file'])
        config_window.port.insert(config['SETTINGS']['Default_port'])
        config_window.ip.insert(config['SETTINGS']['Listen_Address'])
        config_window.save_btn.clicked.connect(save_server_config)

    # Функция сохранения настроек
    def save_server_config():
        global config_window
        message = QMessageBox()
        config['SETTINGS']['Database_path'] = config_window.db_path.text()
        config['SETTINGS']['Database_file'] = config_window.db_file.text()
        try:
            port = int(config_window.port.text())
        except ValueError:
            message.warning(config_window, 'Ошибка', 'Порт должен быть числом')
        else:
            config['SETTINGS']['Listen_Address'] = config_window.ip.text()
            if 1023 < port < 65536:
                config['SETTINGS']['Default_port'] = str(port)
                print(port)
                with open('server.ini', 'w') as conf:
                    config.write(conf)
                    message.information(
                        config_window, 'OK', 'Настройки успешно сохранены!')
            else:
                message.warning(
                    config_window,
                    'Ошибка',
                    'Порт должен быть от 1024 до 65536')

    # Таймер, обновляющий список клиентов 1 раз в секунду
    timer = QTimer()
    timer.timeout.connect(list_update)
    timer.start(1000)

    # Связываем кнопки с процедурами
    main_window.refresh_button.triggered.connect(list_update)
    main_window.show_history_button.triggered.connect(show_statistics)
    main_window.config_btn.triggered.connect(server_config)

    # Запускаем GUI
    app.exec()


if __name__ == '__main__':
    main()
