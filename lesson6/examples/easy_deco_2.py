"""Простейший декоратор-функция"""

import time
import requests


def decorator(func):
    """Сам декоратор"""
    def wrapper():
        """Обертка"""
        start = time.time()
        func()
        end = time.time()
        print(f'Время выполнения исходной ф-ции: {round(end-start, 2)} секунд')
    return wrapper


@decorator
def get_wp():
    """
    получаем ответ сервера
    200 - запрос успешно обработан
    """
    print('Выполняем расчет')
    res = requests.get('https://google.com')
    return res


print(get_wp())
