"""
Подключаем Python-файл с разметкой интерфейса.
Этот файл мы получили через утилиту pyuic.
Пример использования этой утилиты:
pyuic5 test.ui -o test.py
"""

import sys
from PyQt6.QtWidgets import QApplication, QWidget
import test

app = QApplication(sys.argv)
window_obj = QWidget()
ui = test.Ui_Form()
ui.setupUi(window_obj)
ui.btnQuit.clicked.connect(QApplication.quit)
window_obj.show()
sys.exit(app.exec())
