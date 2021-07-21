# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'test.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_mainframe(object):
    def setupUi(self, mainframe):
        mainframe.setObjectName("mainframe")
        mainframe.resize(472, 678)
        font = QtGui.QFont()
        font.setFamily("Ubuntu Condensed")
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        mainframe.setFont(font)
        mainframe.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        mainframe.setStyleSheet("alternate-background-color: rgb(164, 0, 0);\n"
"border-color: rgb(164, 0, 0);")
        self.line = QtWidgets.QFrame(mainframe)
        self.line.setGeometry(QtCore.QRect(10, 50, 451, 16))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.line_2 = QtWidgets.QFrame(mainframe)
        self.line_2.setGeometry(QtCore.QRect(10, 660, 451, 16))
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.frame = QtWidgets.QFrame(mainframe)
        self.frame.setGeometry(QtCore.QRect(10, 290, 451, 111))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.label = QtWidgets.QLabel(self.frame)
        self.label.setGeometry(QtCore.QRect(0, 40, 161, 41))
        self.label.setTextFormat(QtCore.Qt.RichText)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.lineEdit = QtWidgets.QLineEdit(self.frame)
        self.lineEdit.setGeometry(QtCore.QRect(210, 50, 211, 21))
        self.lineEdit.setText("")
        self.lineEdit.setObjectName("lineEdit")
        self.frame_2 = QtWidgets.QFrame(mainframe)
        self.frame_2.setGeometry(QtCore.QRect(10, 430, 451, 111))
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.label_2 = QtWidgets.QLabel(self.frame_2)
        self.label_2.setGeometry(QtCore.QRect(30, 40, 141, 41))
        self.label_2.setObjectName("label_2")
        self.treeView = QtWidgets.QTreeView(self.frame_2)
        self.treeView.setGeometry(QtCore.QRect(200, 50, 211, 21))
        self.treeView.setObjectName("treeView")
        self.label_3 = QtWidgets.QLabel(mainframe)
        self.label_3.setGeometry(QtCore.QRect(20, 20, 161, 31))
        self.label_3.setObjectName("label_3")
        self.pushButton = QtWidgets.QPushButton(mainframe)
        self.pushButton.setGeometry(QtCore.QRect(100, 630, 261, 25))
        self.pushButton.setObjectName("pushButton")
        self.label_4 = QtWidgets.QLabel(mainframe)
        self.label_4.setGeometry(QtCore.QRect(0, 0, 481, 71))
        self.label_4.setStyleSheet("background-color: rgb(164, 0, 0);")
        self.label_4.setText("")
        self.label_4.setObjectName("label_4")
        self.label_4.raise_()
        self.frame.raise_()
        self.line.raise_()
        self.line_2.raise_()
        self.frame_2.raise_()
        self.label_3.raise_()
        self.pushButton.raise_()

        self.retranslateUi(mainframe)
        QtCore.QMetaObject.connectSlotsByName(mainframe)

    def retranslateUi(self, mainframe):
        _translate = QtCore.QCoreApplication.translate
        mainframe.setWindowTitle(_translate("mainframe", "vulndork"))
        self.label.setText(_translate("mainframe", "Enter web-site url:"))
        self.label_2.setText(_translate("mainframe", "Enter dorks file path:"))
        self.label_3.setText(_translate("mainframe", "<html><head/><body><p><img src=\":/home/cymed/Downloads/Webp.net-resizeimage(1).png\"/></p></body></html>"))
        self.pushButton.setText(_translate("mainframe", "Start the scan"))

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    mainframe = QtWidgets.QDialog()
    ui = Ui_mainframe()
    ui.setupUi(mainframe)
    mainframe.show()
    sys.exit(app.exec_())
