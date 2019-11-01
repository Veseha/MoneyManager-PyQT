import sys
from PyQt5.QtGui import QPalette, QTextCursor, QPainter, QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QCheckBox, QGridLayout, QTextEdit
from PyQt5.QtWidgets import QLCDNumber, QLineEdit, QMainWindow
from PyQt5 import uic
from PyQt5.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        uic.loadUi('main.ui', self)
        # self.setMouseTracking(True)

    def initUI(self):
        self.im1 = 'icon/plus.ico'
        p1 = QPixmap(self.im1)
        self.plus.setIcon(p1)




if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec())
