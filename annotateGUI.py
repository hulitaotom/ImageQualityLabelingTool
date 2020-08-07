# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'annotateGUI.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from QtImageViewer import QtImageViewer

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        ratio = 1.0
        MainWindow.resize(1800*ratio, 956)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        #self.imageView = QtWidgets.QGraphicsView(self.centralwidget)
        self.imageView = QtImageViewer(self.centralwidget)
        self.imageView.setGeometry(QtCore.QRect(10, 10, 711*ratio, 921*ratio))
        self.imageView.setObjectName("imageView")
        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setGeometry(QtCore.QRect(730*ratio, 60, 1041*ratio, (800)*ratio))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(9)
        self.tableWidget.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)
        
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(6, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(7, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(8, item)
        
        self.cboFileList = QtWidgets.QComboBox(self.centralwidget)
        self.cboFileList.setGeometry(QtCore.QRect(730*ratio, 10, 200, 40))
        self.cboFileList.setObjectName("cboFileList")
        self.btnNextImage = QtWidgets.QPushButton(self.centralwidget)
        self.btnNextImage.setGeometry(QtCore.QRect(860+750*(ratio-1), 870, 111, 51))
        self.btnNextImage.setObjectName("btnNextImage")
        self.btnSave = QtWidgets.QPushButton(self.centralwidget)
        self.btnSave.setGeometry(QtCore.QRect(860+750*(ratio-1)+200, 900, 93, 28))
        self.btnSave.setObjectName("btnSave")
        self.lineSaveStatus = QtWidgets.QLineEdit(self.centralwidget)
        self.lineSaveStatus.setGeometry(QtCore.QRect(860+750*(ratio-1)+190, 870, 113, 22))
        self.lineSaveStatus.setObjectName("lineSaveStatus")
        #self.btnUndo = QtWidgets.QPushButton(self.centralwidget)
        #self.btnUndo.setGeometry(QtCore.QRect(860+750*(ratio-1)+400, 850+600, 93, 28))
        #self.btnUndo.setObjectName("btnUndo")
        self.btnPrevImage = QtWidgets.QPushButton(self.centralwidget)
        self.btnPrevImage.setGeometry(QtCore.QRect(750*ratio, 870, 111, 51))
        self.btnPrevImage.setObjectName("btnPrevImage")
        '''
        self.cboPageRank = QtWidgets.QComboBox(self.centralwidget)
        self.cboPageRank.setGeometry(QtCore.QRect(730*ratio+400, 111, 111, 41))
        self.cboPageRank.setObjectName("cboPageRank")
        self.cboPageRank.addItem("")
        self.cboPageRank.addItem("")
        self.cboPageRank.addItem("")
        self.cboPageRank.addItem("")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(730*ratio+400, 80, 100, 30))
        self.label.setObjectName("label")
        '''
        self.labelVersion = QtWidgets.QLabel(self.centralwidget)
        self.labelVersion.setGeometry(QtCore.QRect(860+750*(ratio-1)+500, 900, 91, 20))
        font = QtGui.QFont()
        font.setPointSize(7)
        self.labelVersion.setFont(font)
        self.labelVersion.setObjectName("labelVersion")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(860+750*(ratio-1)+500, 880, 310, 20))
        font = QtGui.QFont()
        font.setPointSize(7)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1686, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Show"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "ROI Coords."))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Type"))
        
        item = self.tableWidget.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "300DPI"))
        item = self.tableWidget.horizontalHeaderItem(4)
        item.setText(_translate("MainWindow", "200DPI"))
        item = self.tableWidget.horizontalHeaderItem(5)
        item.setText(_translate("MainWindow", "150DPI"))
        item = self.tableWidget.horizontalHeaderItem(6)
        item.setText(_translate("MainWindow", "100DPI"))
        item = self.tableWidget.horizontalHeaderItem(7)
        item.setText(_translate("MainWindow", "75DPI"))
        item = self.tableWidget.horizontalHeaderItem(8)
        item.setText(_translate("MainWindow", "Comments"))
        
        self.btnNextImage.setText(_translate("MainWindow", "Next Image"))
        self.btnSave.setText(_translate("MainWindow", "Save"))
        #self.btnUndo.setText(_translate("MainWindow", "Undo"))
        self.btnPrevImage.setText(_translate("MainWindow", "Prev Image"))
        '''
        self.cboPageRank.setItemText(0, _translate("MainWindow", "A"))
        self.cboPageRank.setItemText(1, _translate("MainWindow", "B"))
        self.cboPageRank.setItemText(2, _translate("MainWindow", "C"))
        self.cboPageRank.setItemText(3, _translate("MainWindow", "D"))
        self.label.setText(_translate("MainWindow", "Page Rank"))
        '''
        self.labelVersion.setText(_translate("MainWindow", "Ver. 200410"))
        self.label_4.setText(_translate("MainWindow", "@Electronic Imaging Systems Laboratory "))

