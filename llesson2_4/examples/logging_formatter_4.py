"""
Журналирование (логгирование) с использованием модуля logging
Расширенная настройка. Форматирование, обработчики
"""

import sys
import logging

# Создать логгер - регистратор верхнего уроовня
# с именем app
APP_LOG = logging.getLogger('app')
# Установить уровень важности
APP_LOG.setLevel(logging.INFO)

# Создать обработчик который выводит сообщения с уровнем CRITICAL в поток stderr
STREAM_HANDLER = logging.StreamHandler(sys.stderr)
STREAM_HANDLER.setLevel(logging.INFO)

# Создать обработчик который выводит сообщения в файл
FILE_HANDLER = logging.FileHandler('app_4.log')
FILE_HANDLER.setLevel(logging.INFO)

# Создать объект Formatter
# Определить формат сообщений
FORMATTER = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s ")

# подключить объект Formatter к обработчикам
STREAM_HANDLER.setFormatter(FORMATTER)
FILE_HANDLER.setFormatter(FORMATTER)

# Добавить обработчики к регистратору
APP_LOG.addHandler(STREAM_HANDLER)
APP_LOG.addHandler(FILE_HANDLER)

# Передать сообщение обработчику
APP_LOG.info('Замечательный день для релиза!')
