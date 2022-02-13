# Выполнить пинг веб-ресурсов yandex.ru, youtube.com
# и преобразовать результаты из байтовового в строковый тип на кириллице.
import platform
import subprocess


def main():
    sites = ['yandex.ru', 'youtube.com']
    param = '-n' if platform.system().lower() == 'windows' else '-c'
    for site in sites:
        args = ['ping', param, '2', site]
        result = subprocess.Popen(args, stdout=subprocess.PIPE)
        for line in result.stdout:
            print(line.decode('cp1251'))


if __name__ == '__main__':
    main()
