"""
Подключаем файл с разметкой интерфейса, созданного через qtdesigner
(вариант без создания класса MyWindow)
"""

import sys
from PyQt6.QtWidgets import QWidget, QApplication
from PyQt6 import uic


app = QApplication(sys.argv)
window_obj = QWidget()
UI = uic.loadUi('test.ui', window_obj)
UI.btnQuit.clicked.connect(QApplication.quit)
window_obj.show()

sys.exit(app.exec())
