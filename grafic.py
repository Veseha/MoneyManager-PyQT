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
        self.listmoneyMax = 0
        self.timesMoney = 0

        for i in self.listmoney:            # Чекает на максимальное число,
            self.timesMoney += i            # нужно для создания "верхушки" графика
            if self.timesMoney > self.listmoneyMax:
                self.listmoneyMax = self.timesMoney
            elif 0 - self.timesMoney > self.listmoneyMax:
                self.listmoneyMax = 0 - self.timesMoney
        if self.firstmoney > 0:
            self.listmoneyMax += self.firstmoney
        self.max.setText(str(self.listmoneyMax))
        self.min.setText('-' + str(self.listmoneyMax))
        self.sredplus.setText(str(self.listmoneyMax / 2))
        self.sredminus.setText('-' + str(self.listmoneyMax / 2))

    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        self.drawstart(qp)
        qp.end()

    def oneShag(self):
        shagY = (self.listmoneyMax + 10) / 250   # определяет количество шагов по принципу
        shagX = 480 / len(self.listmoney)        # n денег = k шагов, для автоматического
        return shagX, shagY                     # адаптирования графика

    def drawstart(self, qp):
        pen = QPen(Qt.black, 2, Qt.SolidLine)
        pen.setStyle(Qt.DotLine)
        qp.setPen(pen)
        qp.drawLine(10, 250, 490, 250)

        pen = QPen(Qt.red, 4, Qt.SolidLine)
        qp.setPen(pen)

        sX, sY = self.oneShag()
        if self.firstmoney == 0:    # Проверка на то, было ли первая сумма( в самом начале) нулем.
            corr = [10, 250]
        else:                       # А если нет, то ставит первые кординаты соотвествующие
            yFirst = 250 - self.firstmoney / sY
            corr = [10, yFirst]     # сorr это начало следущей линии

        lastChi = self.firstmoney
        for i in range(len(self.listmoney)):   # сам алгоритм построения графика, работает - не лезь
            corrY = lastChi + self.listmoney[i]
            x = (i + 1) * sX
            if self.listmoney[i] > 0:
                pen = QPen(Qt.green, 4, Qt.SolidLine)
                qp.setPen(pen)
                y = 250 - corrY / sY

            else:
                pen = QPen(Qt.red, 4, Qt.SolidLine)
                qp.setPen(pen)
                y = (0 - corrY) / sY + 250

            lastChi = corrY

            qp.drawLine(corr[0], corr[1], x, y)
            pen = QPen(Qt.black, 6)
            qp.setPen(pen)
            qp.drawPoint(x, y)
            qp.drawPoint(corr[0], corr[1])
            corr = [x, y]
        print('the end')





