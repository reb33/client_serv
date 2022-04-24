"""
Простейшее логгирование
"""

import logging

# Создаём объект-логгер с именем app.main
LOG = logging.getLogger('app.main')

# Создаём объект форматирования:
FORMATTER = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s ")

# Создаём файловый обработчик логгирования (можно задать кодировку):
FILE_HANDLER = logging.FileHandler("app.main.log", encoding='utf-8')
#fh.setLevel(logging.DEBUG)
FILE_HANDLER.setFormatter(FORMATTER)

# Добавляем в логгер новый обработчик событий и устанавливаем уровень логгирования
LOG.addHandler(FILE_HANDLER)
LOG.setLevel(logging.DEBUG)

if __name__ == '__main__':
    # Создаём потоковый обработчик логгирования (по умолчанию sys.stderr):
    STREAM_HANDLER = logging.StreamHandler()
    #console.setLevel(logging.DEBUG)
    STREAM_HANDLER.setFormatter(FORMATTER)
    LOG.addHandler(STREAM_HANDLER)
    # В логгирование передаем имя текущей функции и имя вызвавшей функции
    LOG.debug('Отладочное сообщение')
