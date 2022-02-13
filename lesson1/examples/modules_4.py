"""
Модуль subprocess
"""

import chardet   # необходима предварительная инсталляция!
import subprocess
import platform


param = '-n' if platform.system().lower() == 'windows' else '-c'
args = ['ping', param, '2', 'yandex.ru']
result = subprocess.Popen(args, stdout=subprocess.PIPE)
for line in result.stdout:
    result = chardet.detect(line)
    line = line.decode(result['encoding']).encode('utf-8')
    print(line.decode('utf-8'))


# =====================================================
# # определение кодировки системы по умолчанию
import locale
default_encoding = locale.getpreferredencoding()
print(default_encoding)
