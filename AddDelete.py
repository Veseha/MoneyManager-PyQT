from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QMessageBox
from PyQt5 import uic
from Directory import basesqlite3
import sqlite3
from PyQt5.QtCore import Qt


class Create(QWidget):
    def __init__(self, parent=None):
        super(Create, self).__init__(parent)
        self.setWindowFlags(Qt.Window)
        self.parent = parent
        uic.loadUi('newscoreW.ui', self)
        self.base = sqlite3.connect(basesqlite3)
        self.setWindowTitle('Добавление Счета')
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Create score')
        self.lineEdit.setText('Новый счет')
        self.lineEdit_2.setText('0')
        self.pushButton.clicked.connect(self.NewSchet)
        self.pushButton_2.clicked.connect(self.close)

    def NewSchet(self):
        mon = int(self.lineEdit_2.text())
        nam = self.lineEdit.text()
        cur1 = self.base.cursor()
        a = cur1.execute('''SELECT s.name FROM score AS s WHERE s.name == "{}"'''.format(nam)).fetchall()
        if not a:
            cur = self.base.cursor()
            cur.execute("INSERT INTO score(name, money, firstmon) "
                        "VALUES('{}', {}, {}) ".format(nam, mon, mon))
            self.base.commit()
            message = QMessageBox()
            message.setIcon(QMessageBox.Information)
            message.setText('Счет успешно создан!')
            message.setWindowTitle('Информация')
            message.setStandardButtons(QMessageBox.Ok)
            # returnValue = message.exec()
            message.exec()
            self.parent.changeComboBox()
            self.close()
        else:
            message1 = QMessageBox()
            message1.setIcon(QMessageBox.Warning)
            message1.setText('Данное название уже используется.\n Пожалуйста, '
                             'выберите другое название')
            message1.setWindowTitle('Информация')
            message1.setStandardButtons(QMessageBox.Ok)
            # returnValue = message1.exec()
            message1.exec()


class Delete(QWidget):
    def __init__(self, parent=None):
        super(Delete, self).__init__(parent)
        self.setWindowFlags(Qt.Window)
        self.parent = parent
        uic.loadUi('deleteW.ui', self)
        self.base = sqlite3.connect(basesqlite3)
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Delete score')
        self.cur2 = self.base.cursor()
        namescored = self.cur2.execute('SELECT name FROM score').fetchall()
        list_of_name = []
        for i in namescored:
            list_of_name.append(i[0])
        self.comboBox.addItems(list_of_name)
        self.pushButton.clicked.connect(self.deleteScore)
        self.pushButton_2.clicked.connect(self.close)

    def deleteScore(self):
        name = self.comboBox.currentText()
        cur = self.base.cursor()
        cur.execute('DELETE from operation WHERE scorename == "{}"'.format(name))
        cur.execute('DELETE from score WHERE name == "{}"'.format(name)).fetchall()
        self.base.commit()
        self.base.close()
        message = QMessageBox()
        message.setIcon(QMessageBox.Information)
        message.setText('Счет удален')
        message.setWindowTitle('Информация')
        message.setStandardButtons(QMessageBox.Ok)
        message.exec()
        self.parent.changeComboBox()
        self.close()
