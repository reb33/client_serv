"""
Сервер времени, обрабатывающий "одновременно" несколько клиентов
Обработка клиентов осуществляется функцией select
"""

import time
import select
from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR


def new_listen_socket(address):
    """Инициируем серверный сокет"""
    sock = socket(AF_INET, SOCK_STREAM)
    sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    sock.bind(address)
    sock.listen(5)
    # проверяем есть ли новые клиенты
    # проверяем есть ли данные
    sock.settimeout(1)
    return sock


def mainloop():
    """Основной цикл обработки запросов клиентов"""
    address = ('', 8888)
    all_clients = []
    sock = new_listen_socket(address)

    while True:
        try:
            # Проверка подключений
            conn, addr = sock.accept()
            print(conn)
        # timeout вышел
        except OSError as err:
            print(f'OSError code on the server side is : {err.errno}')
            # The error number returns None because it's just a timeout
            pass
        else:
            print(f"Получен запрос на соединение с {str(addr)}")
            # вносим в список добавившегося клиента
            all_clients.append(conn)
        finally:

            clients_write = []
            try:
                clients_read, clients_write, errors = select.select([], all_clients, [], 0)

            except Exception as e:
                print(e)
                pass

            for client in clients_write:
                # определяем время
                time_str = time.ctime(time.time()) + "\n"
                try:
                    # отправляем время клиенту
                    client.send(time_str.encode('utf-8'))

                except Exception as e:
                    print(e)
                    # клиент отключился
                    all_clients.remove(client)
                    client.close()


print('Эхо-сервер запущен!')
mainloop()
