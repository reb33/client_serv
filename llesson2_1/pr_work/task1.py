# 1. Написать функцию host_ping(),
# в которой с помощью утилиты ping будет проверяться доступность сетевых узлов.
# Аргументом функции является список, в котором каждый сетевой узел должен быть представлен
# именем хоста или ip-адресом. В функции необходимо перебирать ip-адреса и проверять их доступность
# с выводом соответствующего сообщения («Узел доступен», «Узел недоступен»).
# При этом ip-адрес сетевого узла должен создаваться с помощью функции ip_address().
# (Внимание! Аргументом сабпроцеса должен быть список, а не строка!!! Крайне желательно использование потоков.)
import platform
from threading import Thread
from ipaddress import ip_address
from subprocess import Popen, PIPE


def ping(ip, res: list):
    param = '-n' if platform.system().lower() == 'windows' else '-c'
    args = ['ping', param, '1', ip]
    reply = Popen(args, stdout=PIPE, stderr=PIPE)

    code = reply.wait()
    if code == 0:
        res.append('Узел доступен')
    else:
        res.append('Узел недоступен')
    return


def host_ping(list_ip):
    list_treads = {}
    for ip in list_ip:
        res = []
        thread = Thread(target=ping, args=(ip, res))
        list_treads[ip] = (thread, res)
        thread.start()

    results = {}
    for ip, (t, res) in list_treads.items():
        t.join()
        results[ip] = res[0]

    return results


if __name__ == '__main__':
    ip1 = ip_address('8.8.8.0')
    ip_addrs = map(str, [ip1+i for i in range(10)])
    print(host_ping(ip_addrs))
