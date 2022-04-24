"""
Журналирование (логгирование) с использованием модуля logging
асширенная настройка. Форматирование, обработчики
"""

import logging

# Создать логгер - регистратор верхнего уроовня
# с именем app.main
LOG = logging.getLogger('app')

# Создать обработчик
FILE_HANDLER = logging.FileHandler("app_2.log", encoding='utf-8')
# выводит сообщения с уровнем DEBUG
FILE_HANDLER.setLevel(logging.DEBUG)

# Создать объект Formatter
# Определить формат сообщений
FORMATTER = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

# подключить объект Formatter к обработчику
FILE_HANDLER.setFormatter(FORMATTER)

PARAMS = {'host': 'www.python.org', 'port': 80}

# Добавить обработчик к регистратору
LOG.addHandler(FILE_HANDLER)
LOG.setLevel(logging.DEBUG)

# Передать сообщение обработчику
#log.info('Замечательный день для релиза!')
LOG.info("Параметры подключения: %(host)s, %(port)d", PARAMS)
