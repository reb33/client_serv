# 3. Задание на закрепление знаний по модулю yaml.
# Написать скрипт, автоматизирующий сохранение данных в файле YAML-формата. Для этого:
# Подготовить данные для записи в виде словаря, в котором первому ключу соответствует список,
# второму — целое число, третьему — вложенный словарь,
# где значение каждого ключа — это целое число с юникод-символом, отсутствующим в кодировке ASCII (например, €);
# Реализовать сохранение данных в файл формата YAML — например, в файл file.yaml.
# При этом обеспечить стилизацию файла с помощью параметра default_flow_style,
# а также установить возможность работы с юникодом: allow_unicode = True;
# Реализовать считывание данных из созданного файла и проверить, совпадают ли они с исходными.
import yaml


def write_to_yaml(data):
    with open('file.yaml', 'w') as file:
        yaml.dump(data, file, default_flow_style=False, allow_unicode=True)


def main():
    write_to_yaml({
        'key1': ['val1', 'val2', 'val3'],
        'key2': 42,
        'key3': {
            '32\u00d8': 'it\'s diameter',
            '33\u220f': 'it\'s Pi',
            '34\uf8ff': 'it\'s apple'
        }
    })


if __name__ == '__main__':
    main()
