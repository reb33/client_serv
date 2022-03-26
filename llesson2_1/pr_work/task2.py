# Написать функцию host_range_ping() (возможности которой основаны на функции из примера 1)
# для перебора ip-адресов из заданного диапазона.
# Меняться должен только последний октет каждого адреса.
# По результатам проверки должно выводиться соответствующее сообщение.
from ipaddress import ip_address

from task1 import host_ping


def host_range_ping(start_ip: str, end_ip: str):
    start = ip_address(start_ip)
    end = ip_address(end_ip)
    if start_ip[:start_ip.rfind('.')] != end_ip[:start_ip.rfind('.')]:
        print('Адреса не из одной подсети')
        return
    if end <= start:
        print('Второй адрес должен быть больще первого')
        return
    diff = int(end_ip.split('.')[3]) - int(start_ip.split('.')[3])
    ip_list = map(str, [start + i for i in range(diff)])
    return host_ping(ip_list)


if __name__ == '__main__':
    print(host_range_ping('8.8.8.0', '8.8.8.20'))
