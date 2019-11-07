import sys
from PyQt5 import QtGui
from PyQt5.QtGui import QPalette, QTextCursor, QPixmap, QPainter, QPen
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QCheckBox, QGridLayout, QTextEdit
from PyQt5.QtWidgets import QLCDNumber, QLineEdit, QMainWindow
from PyQt5 import uic
from PyQt5.QtCore import Qt
from Directory import basesqlite3
import sqlite3




class Grafic(QWidget):
    def __init__(self, name_score):
        super().__init__()
        uic.loadUi('graficA.ui', self)
        self.check = False
        self.sizeimage = [500, 500]
        self.name_score = name_score
        self.base = sqlite3.connect(basesqlite3)
        cur = self.base.cursor()
        a = cur.execute('''SELECT summ FROM operation 
                    WHERE scorename == "{}"'''.format(self.name_score)).fetchall()
        self.listmoney = [i[0] for i in a]

        self.firstmoney = cur.execute('''SELECT firstmon FROM score
                    WHERE name == "{}"'''.format(self.name_score)).fetchone()[0]
        self.scoremoney = cur.execute('''SELECT money FROM score 
        WHERE name == "{}"'''.format(self.name_score)).fetchone()[0]
        self.initUI()


    def initUI(self):
        self.angle = [(500, 500), (-500, 500), (-500, -500), (500, -500)]
        self.listmoneyMax = sorted(self.listmoney)[-1]

    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        self.drawstart(qp)
        qp.end()

    def oneShag(self):
        shagY = self.listmoneyMax / 250
        shagX = 480 / len(self.listmoney)

        return shagX, shagY

    def drawstart(self, qp):
        pen = QPen(Qt.black, 2, Qt.SolidLine)
        pen.setStyle(Qt.DotLine)
        qp.setPen(pen)
        qp.drawLine(10, 250, 490, 250)

        pen = QPen(Qt.red, 4, Qt.SolidLine)
        qp.setPen(pen)
        corr = [10, 250]
        sX, sY = self.oneShag()
        for i in range(len(self.listmoney)):
            pen = QPen(Qt.red, 4, Qt.SolidLine)
            qp.setPen(pen)
            x = (i + 1) * sX
            if self.listmoney[i] > 0:
                y = self.listmoney[i] * sY + 1
                print(sY)
            else:
                y = 500 - ((0 - self.listmoney[i]) * sY)
            print(self.listmoney[i], '-------',  x, y)
            qp.drawLine(corr[0], corr[1], x, y)
            pen = QPen(Qt.black, 6)
            qp.setPen(pen)
            qp.drawPoint(x, y)
            corr = [x, y]




