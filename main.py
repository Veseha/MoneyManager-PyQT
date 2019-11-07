import sqlite3
import sys
from PyQt5.QtGui import QPixmap, QCursor
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow, QMessageBox
from PyQt5 import uic
from PyQt5 import QtCore
from customfunc import QPicButton
from os import name as OSname
from grafic import Grafic
from static import Static
from AddDelete import Create, Delete
from PlusMinus import Plus, Minus
from Directory import basesqlite3

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        # self.setMouseTracking(True)
        self.initUI()

    def initUI(self):
        if OSname != 'nt':
            message = QMessageBox()
            message.setIcon(QMessageBox.Information)
            message.setText('Установите шрифт Bahnschrift Condensed')
            message.setWindowTitle('Information')
            message.setStandardButtons(QMessageBox.Ok)
            returnValue = message.exec()

        self.setWindowTitle('Money Manager by Veseha')

        self.plus1 = QPicButton(QPixmap('icon/plus.ico'), QPixmap('icon/plus12.png'), self)
        self.plus1.setGeometry(100, 110, 100, 100)
        self.plus1.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.plus1.clicked.connect(self.plusW)

        self.minus1 = QPicButton(QPixmap('icon/minus.ico'), QPixmap('icon/minus12.png'), self)
        self.minus1.setGeometry(280, 110, 100, 100)
        self.minus1.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.minus1.clicked.connect(self.minusW)

        self.create1 = QPicButton(QPixmap('icon/add.png'), QPixmap('icon/add12.png'), self)
        self.create1.setGeometry(10, 280, 61, 61)
        self.create1.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.create1.clicked.connect(self.createW)
        # this is working

        self.delete1 = QPicButton(QPixmap('icon/delete.ico'), QPixmap('icon/delete12.ico'), self)
        self.delete1.setGeometry(90, 280, 61, 61)
        self.delete1.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.delete1.clicked.connect(self.deleteW)

        self.grafic1 = QPicButton(QPixmap('icon/diagram.ico'), QPixmap('icon/diagram12.ico'), self)
        self.grafic1.setGeometry(350, 280, 61, 61)
        self.grafic1.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.grafic1.clicked.connect(self.graficW)

        self.static1 = QPicButton(QPixmap('icon/satic.ico'), QPixmap('icon/satic12.ico'), self)
        self.static1.setGeometry(430, 280, 61, 61)
        self.static1.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.static1.clicked.connect(self.staticW)

        self.base = sqlite3.connect(basesqlite3)
        curbase = self.base.cursor()
        a = curbase.execute('SELECT name FROM score').fetchall()
        curbase.close()
        if a:
            self.changeComboBox()
            self.ChangeBudget()
        self.comboBox.activated.connect(self.ChangeBudget)

        self.show()

    def ChangeBudget(self):
        name = self.comboBox.currentText()
        cur_budget = self.base.cursor()
        budget_num = cur_budget.execute('''SELECT s.money FROM score as s WHERE s.name == "{}"'''.format(name)).fetchone()
        self.budget.setText(str(budget_num[0]))

    def changeComboBox(self):
        curbase = self.base.cursor()
        a = curbase.execute('SELECT name FROM score').fetchall()
        curbase.close()
        if a:
            self.comboBox.clear()
            cur = self.base.cursor()
            a = cur.execute('''SELECT s.name FROM score AS s''').fetchall()
            list_of_name = []
            for i in a:
                list_of_name.append(i[0])

            self.comboBox.addItems(list_of_name)
            self.ChangeBudget()
        else:
            self.comboBox.clear()

    def plusW(self):
        self.plusWW = Plus(self, self.comboBox.currentText())
        self.plusWW.show()

    def minusW(self):
        self.minusWW = Minus(self, self.comboBox.currentText())
        self.minusWW.show()

    def createW(self):
        self.createWW = Create(self)
        self.createWW.show()

    def deleteW(self):
        self.deleteWW = Delete(self)
        self.deleteWW.show()

    def graficW(self):
        cur = self.base.cursor()
        a = cur.execute(
            'SELECT * FROM operation WHERE scorename == "{}"'.format(self.comboBox.currentText())).fetchall()
        if a:
            self.graficWW = Grafic(self.comboBox.currentText())
            self.graficWW.show()
        else:
            message = QMessageBox()
            message.setIcon(QMessageBox.Information)
            message.setText('Отсуствуют операции!')
            message.setWindowTitle('Информация')
            message.setStandardButtons(QMessageBox.Ok)
            message.exec()


    def staticW(self):
        cur = self.base.cursor()
        a = cur.execute('SELECT * FROM operation WHERE scorename == "{}"'.format(self.comboBox.currentText())).fetchall()
        if a:
            self.staticWW = Static(self.comboBox.currentText())
            self.staticWW.show()
        else:
            message = QMessageBox()
            message.setIcon(QMessageBox.Information)
            message.setText('Отсуствуют операции!')
            message.setWindowTitle('Информация')
            message.setStandardButtons(QMessageBox.Ok)
            message.exec()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec())
