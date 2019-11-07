from PyQt5.QtWidgets import QWidget, QTableWidgetItem, QMessageBox
from PyQt5 import uic
from Directory import basesqlite3
import sqlite3


class Static(QWidget):
    def __init__(self, name_score):
        super().__init__()
        uic.loadUi('selectstats.ui', self)
        self.name_score = name_score
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Choose statics')
        base = sqlite3.connect(basesqlite3)
        cur = base.cursor()
        a = cur.execute('SELECT * FROM operation WHERE scorename == "{}"'.format(self.name_score)).fetchall()
        if a:
            self.pushButton.clicked.connect(self.AllW)
            self.pushButton_2.clicked.connect(self.DayW)
        else:
            message = QMessageBox()
            message.setIcon(QMessageBox.Information)
            message.setText('Отсуствуют операции!')
            message.setWindowTitle('Информация')
            message.setStandardButtons(QMessageBox.Ok)
            message.exec()
            print('ok')
            message.close()
            self.close()


    def AllW(self):
        self.AllWW = AllStat(self.name_score)
        self.AllWW.show()

    def DayW(self):
        self.DayWW = DayStat(self.name_score)
        self.DayWW.show()


class AllStat(QWidget):
    def __init__(self, name_score):
        super().__init__()
        uic.loadUi('staticall.ui', self)
        self.name_score = name_score
        self.base = sqlite3.connect(basesqlite3)
        self.initUI()


    def initUI(self):
        self.setWindowTitle('Statistic')
        cur = self.base.cursor()
        a = cur.execute('''SELECT o.num FROM operation AS o WHERE scorename == "{}"'''.format(self.name_score)).fetchall()
        self.label_8.setText(str(len(a)))
        b1 = cur.execute('SELECT s.money, s.firstmon FROM score AS s WHERE name == "{}"'.format(self.name_score)).fetchall()
        b2 = b1[0][0] - b1[0][1]
        self.label_9.setText(str(b2))
        c = cur.execute('''SELECT s.summ, s.comment, s.date FROM operation AS s 
        WHERE scorename == "{}"'''.format(self.name_score)).fetchall()
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setHorizontalHeaderLabels(["Сумма", "Коментарий", "Дата "])
        # self.tableWidget.horizontalHeaderItem(0).setToolTip("Номер операции")
        self.tableWidget.horizontalHeaderItem(0).setToolTip("Сумма операции, прибыль или трата(с минусом в начале)")
        self.tableWidget.horizontalHeaderItem(1).setToolTip("Комментарий к операции")
        self.tableWidget.horizontalHeaderItem(2).setToolTip("Дата совершения операции")
        self.tableWidget.setRowCount(len(c))
        for i in range(len(c)):
            self.tableWidget.setItem(i, 0, QTableWidgetItem(str(c[i][0])))
            self.tableWidget.setItem(i, 1, QTableWidgetItem(c[i][1]))
            self.tableWidget.setItem(i, 2, QTableWidgetItem(self.reformDate(c[i][2])))
        self.tableWidget.resizeColumnsToContents()

    def reformDate(self, date):
        date = str(date)
        year, mon, day = date[0:4], date[4:6], date[6:8]
        return year + '.' + mon + '.' + day



class DayStat(QWidget):
    def __init__(self, name_score):
        super().__init__()
        uic.loadUi('staticday.ui', self)
        self.name_score = name_score
        self.base = sqlite3.connect(basesqlite3)
        self.initUI()

    def initUI(self):
        try:
            self.setWindowTitle('Statistic')
            cur = self.base.cursor()
            days = cur.execute('SELECT o.date FROM operation AS o WHERE scorename == "{}"'.format(self.name_score)).fetchall()
            cur.close()
            list_of_name = []
            for i in days:
                if str(i[0]) not in list_of_name:
                    list_of_name.append(str(i[0]))
            self.comboBox.addItems(list_of_name)
            self.comboBox.activated.connect(self.printTable)
            self.comboBox.currentIndexChanged.connect(self.printTable)
        except Exception as e:
            print(e)

    def printTable(self):
            cur = self.base.cursor()
            a = cur.execute('''SELECT o.num FROM operation AS o 
            WHERE date == {}'''.format(self.comboBox.currentText())).fetchall()
            self.label_8.setText(str(len(a)))
            b1 = cur.execute('''SELECT o.summ FROM operation AS o 
            WHERE date == {}'''.format(self.comboBox.currentText())).fetchall()
            b2 = 0
            for i in b1:
                b2 += i[0]
            self.label_9.setText(str(b2))
            c = cur.execute('''SELECT s.summ, s.comment, s.date FROM operation AS s 
            WHERE date == {}'''.format(self.comboBox.currentText())).fetchall()
            self.tableWidget.setColumnCount(3)
            self.tableWidget.setHorizontalHeaderLabels(["Сумма", "Коментарий", "Дата "])
            # self.tableWidget.horizontalHeaderItem(0).setToolTip("Номер операции")
            self.tableWidget.horizontalHeaderItem(0).setToolTip("Сумма операции, прибыль или трата(с минусом в начале)")
            self.tableWidget.horizontalHeaderItem(1).setToolTip("Комментарий к операции")
            self.tableWidget.horizontalHeaderItem(2).setToolTip("Дата совершения операции")
            self.tableWidget.setRowCount(len(c))
            for i in range(len(c)):
                self.tableWidget.setItem(i, 0, QTableWidgetItem(str(c[i][0])))
                self.tableWidget.setItem(i, 1, QTableWidgetItem(c[i][1]))
                self.tableWidget.setItem(i, 2, QTableWidgetItem(self.reformDate(c[i][2])))
            self.tableWidget.resizeColumnsToContents()

    def reformDate(self, date):
        date = str(date)
        year, mon, day = date[0:4], date[4:6], date[6:8]
        return year + '.' + mon + '.' + day
