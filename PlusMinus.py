import sqlite3
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QMessageBox
from PyQt5 import uic
from Directory import basesqlite3
import datetime
from PyQt5.QtCore import Qt


class Plus(QWidget):
    def __init__(self, parent, name_score):
        super(Plus, self).__init__(parent)
        self.setWindowFlags(Qt.Window)
        self.parent = parent
        uic.loadUi('plus.ui', self)
        self.name_score = name_score
        self.base = sqlite3.connect(basesqlite3)
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Add money')
        self.date = datetime.date.today()
        self.date = str(self.date).split('-')
        self.pushButton.clicked.connect(self.newOperation)
        self.pushButton_2.clicked.connect(self.close)
        self.lineEdit.setText('1')
        self.yeart.setText(self.date[0])
        self.mountht.setText(self.date[1])
        self.dayt.setText(self.date[2])
        self.lineEdit_3.setText('Отсуствует')

    def newOperation(self):
        sum = self.lineEdit.text()
        if len(self.mountht.text()) == 1:
            self.mountht.setText('0' + self.mountht.text())
        if len(self.dayt.text()) == 1:
            self.dayt.setText('0' + self.dayt.text())
        date = ''.join([self.yeart.text(), self.mountht.text(), self.dayt.text()])
        comment = self.lineEdit_3.text()
        if int(sum) <= 0:
            message2 = QMessageBox()
            message2.setIcon(QMessageBox.Warning)
            message2.setText('Введена неправильная сумма!\nПожалуйста, укажите положительное число')
            message2.setWindowTitle('Информация')
            message2.setStandardButtons(QMessageBox.Ok)
            returnValue = message2.exec()
        elif int(self.dayt.text()) > 31 or int(self.dayt.text()) <= 0 or \
            int(self.mountht.text()) > 12 or int(self.mountht.text()) <= 0 or \
            len(self.yeart.text()) != 4:
            message1 = QMessageBox()
            message1.setIcon(QMessageBox.Warning)
            message1.setText('В указанной дате ошибка!\nПожалуйста, следуйте формату год - месяц - день')
            message1.setWindowTitle('Информация')
            message1.setStandardButtons(QMessageBox.Ok)
            returnValue = message1.exec()
        else:
            bum = self.base.cursor()
            a = bum.execute("SELECT o.num FROM operation AS o WHERE scorename == '{}'".format(self.name_score))
            b = len([i[0] for i in a])
            bum.close()

            cur = self.base.cursor()
            cur.execute("UPDATE score SET money = money + {} WHERE name == '{}'".format(int(sum), self.name_score))
            cur.execute("INSERT INTO operation(num, summ, comment, date, scorename) "
                        "VALUES({}, {}, '{}', {}, '{}') ".format(int(b + 1), int(sum), comment, int(date), self.name_score))
            self.base.commit()

            message = QMessageBox()
            message.setIcon(QMessageBox.Information)
            message.setText('Операция добавлена!')
            message.setWindowTitle('Информация')
            message.setStandardButtons(QMessageBox.Ok)
            returnValue = message.exec()
            self.parent.ChangeBudget()
            self.close()

class Minus(QWidget):
    def __init__(self, parent, name_score):
        super(Minus, self).__init__(parent)
        self.setWindowFlags(Qt.Window)
        self.parent = parent
        uic.loadUi('minus.ui', self)
        self.name_score = name_score
        self.base = sqlite3.connect(basesqlite3)
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Spend money')
        self.date = datetime.date.today()
        self.date = str(self.date).split('-')
        self.pushButton.clicked.connect(self.newOperation)
        self.pushButton_2.clicked.connect(self.close)
        self.lineEdit.setText('1')
        self.yeart.setText(self.date[0])
        self.mountht.setText(self.date[1])
        self.dayt.setText(self.date[2])
        self.lineEdit_3.setText('Отсуствует')

    def newOperation(self):
        sum = self.lineEdit.text()
        if len(self.mountht.text()) == 1:
            self.mountht.setText('0' + self.mountht.text())
        if len(self.dayt.text()) == 1:
            self.dayt.setText('0' + self.dayt.text())
        date = ''.join([self.yeart.text(), self.mountht.text(), self.dayt.text()])
        comment = self.lineEdit_3.text()
        if int(sum) <= 0:
            message2 = QMessageBox()
            message2.setIcon(QMessageBox.Warning)
            message2.setText('Введена неправильная сумма!\nПожалуйста, укажите положительное число')
            message2.setWindowTitle('Информация')
            message2.setStandardButtons(QMessageBox.Ok)
            returnValue = message2.exec()
        elif int(self.dayt.text()) > 31 or int(self.dayt.text()) <= 0 or \
                int(self.mountht.text()) > 12 or int(self.mountht.text()) <= 0 or \
                len(self.yeart.text()) != 4:
            message1 = QMessageBox()
            message1.setIcon(QMessageBox.Warning)
            message1.setText('В указанной дате ошибка!\nПожалуйста, следуйте формату год - месяц - день')
            message1.setWindowTitle('Информация')
            message1.setStandardButtons(QMessageBox.Ok)
            returnValue = message1.exec()
        else:
            bum = self.base.cursor()
            a = bum.execute("SELECT o.num FROM operation AS o WHERE scorename == '{}'".format(self.name_score)).fetchall()
            b = len([i[0] for i in a])
            bum.close()

            cur = self.base.cursor()
            cur.execute("UPDATE score SET money = money - {} WHERE name == '{}'".format(int(sum), self.name_score))
            cur.execute("INSERT INTO operation(num, summ, comment, date, scorename) "
                        "VALUES({}, {}, '{}', {}, '{}') ".format(int(b + 1), -int(sum), comment, int(date),
                                                                 self.name_score))
            self.base.commit()

            message = QMessageBox()
            message.setIcon(QMessageBox.Information)
            message.setText('Операция добавлена!')
            message.setWindowTitle('Информация')
            message.setStandardButtons(QMessageBox.Ok)
            returnValue = message.exec()
            self.parent.ChangeBudget()
            self.close()