"""Простейшее главное окно с разметкой и запуском"""

import sys
from PyQt6.QtWidgets import QMainWindow, QApplication
from PyQt6.QtGui import QIcon, QAction


class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Действие (Action) будет совершаться при нажатии на кнопку
        exitAction = QAction(QIcon('exit.png'), 'Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.triggered.connect(QApplication.quit)

        # Создание кнопки на панели инструментов
        self.toolbar = self.addToolBar('Exit')
        self.toolbar.addAction(exitAction)

        # Установка заголовка и размеров главного окна
        self.setGeometry(700, 300, 300, 200)
        self.setWindowTitle('Toolbar')
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec())
