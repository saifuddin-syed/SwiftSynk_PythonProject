

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1080, 740)
        MainWindow.setStyleSheet("#widget1{\n"
"    background-color: rgb(106, 90, 205)\n"
"}\n"
"\n"
"#table{\n"
"    background-color: rgb(194, 194, 255);\n"
"    border-width: 0px;\n"
"    gridline-color: rgb(194, 194, 255)\n"
"}\n"
"\n"
"#table2{\n"
"    background-color: rgb(194, 194, 255);\n"
"    border-width: 0px;\n"
"    gridline-color: rgb(194, 194, 255)\n"
"}\n"
"\n"
"#syncButton{\n"
"    background-color: rgb(106, 90, 205);\n"
"    border-top-left-radius: 12;\n"
"    border-bottom-left-radius: 12;\n"
"    color: white\n"
"}\n"
"\n"
"#syncButton2{\n"
"    background-color: rgb(106, 90, 205);\n"
"    border-top-right-radius: 12;\n"
"    border-bottom-right-radius: 12;\n"
"    color: white;\n"
"    border-left-color: rgb(255, 255, 255)\n"
"}\n"
"#backbutton{\n"
"    background-color: rgb(106, 90, 205);\n"
"    border-radius: 5;\n"
"    border: none;\n"
"    color: white\n"
"}\n"
"\n"
"")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.widget1 = QtWidgets.QWidget(self.centralwidget)
        self.widget1.setGeometry(QtCore.QRect(0, 0, 1082, 62))
        self.widget1.setStyleSheet("")
        self.widget1.setObjectName("widget1")
        self.stackedWidget = QtWidgets.QStackedWidget(self.centralwidget)
        self.stackedWidget.setGeometry(QtCore.QRect(0, 58, 1082, 682))
        self.stackedWidget.setObjectName("stackedWidget")
        self.page = QtWidgets.QWidget()
        self.page.setObjectName("page")
        self.table = QtWidgets.QTableWidget(self.page)
        self.table.setGeometry(QtCore.QRect(0, 0, 1082, 682))
        self.table.setStyleSheet("QHeaderView::section {\n"
"    background-color: rgb(255, 255, 255);\n"
"    border: none\n"
"}")
        self.table.setObjectName("table")
        self.table.verticalHeader().setVisible(False)
        self.table.setColumnCount(5)
        self.table.setColumnWidth(0, 50)
        self.table.setColumnWidth(1, 150)
        self.table.setColumnWidth(2, 100)
        self.table.setColumnWidth(3, 400)
        self.table.setColumnWidth(4, 100)
        self.table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.table.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.table.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.table.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.table.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.table.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.table.setHorizontalHeaderItem(4, item)
        self.syncButton = QtWidgets.QPushButton(self.page)
        self.syncButton.setGeometry(QtCore.QRect(880, 560, 90, 102))
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.syncButton.setFont(font)
        self.syncButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.syncButton.setObjectName("syncButton")
        self.syncButton2 = QtWidgets.QPushButton(self.page)
        self.syncButton2.setGeometry(QtCore.QRect(972, 560, 90, 102))
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.syncButton2.setFont(font)
        self.syncButton2.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.syncButton2.setStyleSheet("#syncButton2{\n"
"    text : SYNC \\n Folder\n"
"}")
        self.syncButton2.setObjectName("syncButton2")
        self.stackedWidget.addWidget(self.page)
        self.page_2 = QtWidgets.QWidget()
        self.page_2.setObjectName("page_2")
        self.table2 = QtWidgets.QTableWidget(self.page_2)
        self.table2.setGeometry(QtCore.QRect(0, 0, 1082, 682))
        self.table2.setStyleSheet("QHeaderView::section {\n"
"    background-color: rgb(255, 255, 255);\n"
"    border: none\n"
"}")
        self.table2.setObjectName("table2")
        self.table2.verticalHeader().setVisible(False)
        self.table2.setColumnCount(5)
        self.table2.setColumnWidth(0, 50)
        self.table2.setColumnWidth(1, 150)
        self.table2.setColumnWidth(2, 100)
        self.table2.setColumnWidth(3, 400)
        self.table2.setColumnWidth(4, 100)
        self.table2.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.table2.setColumnCount(5)
        self.table2.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.table2.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.table2.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.table2.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.table2.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.table2.setHorizontalHeaderItem(4, item)
        self.backbutton = QtWidgets.QPushButton(self.page_2)
        self.backbutton.setGeometry(QtCore.QRect(920, 620, 112, 42))
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.backbutton.setFont(font)
        self.backbutton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.backbutton.setObjectName("backbutton")
        self.stackedWidget.addWidget(self.page_2)
        self.page_3 = QtWidgets.QWidget()
        self.page_3.setObjectName("page_3")
        self.stackedWidget.addWidget(self.page_3)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        self.stackedWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        item = self.table.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Name"))
        item = self.table.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Status"))
        item = self.table.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "Path"))
        item = self.table.horizontalHeaderItem(4)
        item.setText(_translate("MainWindow", "Size"))
        self.syncButton.setToolTip(_translate("MainWindow", "Select files to Sync"))
        self.syncButton.setText(_translate("MainWindow", "SYNC\n"
"Files"))
        self.syncButton2.setText(_translate("MainWindow", "SYNC\n"
"Folders"))
        item = self.table2.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Name"))
        item = self.table2.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Status"))
        item = self.table2.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "Path"))
        item = self.table2.horizontalHeaderItem(4)
        item.setText(_translate("MainWindow", "Size"))
        self.backbutton.setText(_translate("MainWindow", "◀ Back"))
        self.backbutton.setToolTip(_translate("MainWindow", "Go Back to Files"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())