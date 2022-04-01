# Написать функцию host_range_ping_tab(), возможности которой основаны на функции из примера 2.
# Но в данном случае результат должен быть итоговым по всем ip-адресам,
# представленным в табличном формате (использовать модуль tabulate).
# Таблица должна состоять из двух колонок
from tabulate import tabulate

from task2 import host_range_ping


def host_range_ping_tab(start_ip, end_ip):
    result = [(k, v) for k, v in host_range_ping(start_ip, end_ip).items()]
    print(tabulate(result, headers=('ip', 'Доступность')))


if __name__ == '__main__':
    host_range_ping_tab('8.8.8.0', '8.8.8.20')
