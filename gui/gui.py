
# -*- coding: utf-8 -*-

from PyQt4 import QtGui
from PyQt4 import QtCore
import numpy
import sys

class Gui(QtGui.QWidget):

    updGUI=QtCore.pyqtSignal()

    def __init__(self, parent=None):

        QtGui.QWidget.__init__(self, parent)
        #self.setScaledContents(True)
        self.setWindowTitle("Numbers Detection")
        #self.imgLabel=QtGui.QLabel(self)
        self.resize(1000,600)
        self.move(150,50)
        #self.imgLabel.show()
        self.updGUI.connect(self.update)

        #Original Image Label
        self.imgLabel=QtGui.QLabel(self)
        self.imgLabel.resize(500,400)
        self.imgLabel.move(70,50)
        self.imgLabel.show()

        #Transform Image Label
        self.transLabel=QtGui.QLabel(self)
        self.transLabel.resize(200,200)
        self.transLabel.move(700,50)
        self.transLabel.show()

        #Numbers labels 1 to 10
        self.lab1=QtGui.QLabel(self)
        self.lab1.resize(30,30)
        self.lab1.move(700,300)
        self.lab1.setText('1')
        self.lab1.setAlignment(QtCore.Qt.AlignCenter)
        self.lab1.setStyleSheet("background-color: #7FFFD4; color: #000; font-size: 20px; border: 1px solid black;")

        self.lab2=QtGui.QLabel(self)
        self.lab2.resize(30,30)
        self.lab2.move(785,300)
        self.lab2.setText('2')
        self.lab2.setAlignment(QtCore.Qt.AlignCenter)
        self.lab2.setStyleSheet("background-color: #7FFFD4; color: #000; font-size: 20px; border: 1px solid black;")

        self.lab3=QtGui.QLabel(self)
        self.lab3.resize(30,30)
        self.lab3.move(870,300)
        self.lab3.setText('3')
        self.lab3.setAlignment(QtCore.Qt.AlignCenter)
        self.lab3.setStyleSheet("background-color: #7FFFD4; color: #000; font-size: 20px; border: 1px solid black;")

        self.lab4=QtGui.QLabel(self)
        self.lab4.resize(30,30)
        self.lab4.move(700,350)
        self.lab4.setText('4')
        self.lab4.setAlignment(QtCore.Qt.AlignCenter)
        self.lab4.setStyleSheet("background-color: #7FFFD4; color: #000; font-size: 20px; border: 1px solid black;")

        self.lab5=QtGui.QLabel(self)
        self.lab5.resize(30,30)
        self.lab5.move(785,350)
        self.lab5.setText('5')
        self.lab5.setAlignment(QtCore.Qt.AlignCenter)
        self.lab5.setStyleSheet("background-color: #7FFFD4; color: #000; font-size: 20px; border: 1px solid black;")

        self.lab6=QtGui.QLabel(self)
        self.lab6.resize(30,30)
        self.lab6.move(870,350)
        self.lab6.setText('6')
        self.lab6.setAlignment(QtCore.Qt.AlignCenter)
        self.lab6.setStyleSheet("background-color: #7FFFD4; color: #000; font-size: 20px; border: 1px solid black;")

        self.lab7=QtGui.QLabel(self)
        self.lab7.resize(30,30)
        self.lab7.move(700,400)
        self.lab7.setText('7')
        self.lab7.setAlignment(QtCore.Qt.AlignCenter)
        self.lab7.setStyleSheet("background-color: #7FFFD4; color: #000; font-size: 20px; border: 1px solid black;")

        self.lab8=QtGui.QLabel(self)
        self.lab8.resize(30,30)
        self.lab8.move(785,400)
        self.lab8.setText('8')
        self.lab8.setAlignment(QtCore.Qt.AlignCenter)
        self.lab8.setStyleSheet("background-color: #7FFFD4; color: #000; font-size: 20px; border: 1px solid black;")

        self.lab9=QtGui.QLabel(self)
        self.lab9.resize(30,30)
        self.lab9.move(870,400)
        self.lab9.setText('9')
        self.lab9.setAlignment(QtCore.Qt.AlignCenter)
        self.lab9.setStyleSheet("background-color: #7FFFD4; color: #000; font-size: 20px; border: 1px solid black;")

        self.lab0=QtGui.QLabel(self)
        self.lab0.resize(30,30)
        self.lab0.move(785,450)
        self.lab0.setText('0')
        self.lab0.setAlignment(QtCore.Qt.AlignCenter)
        self.lab0.setStyleSheet("background-color: #7FFFD4; color: #000; font-size: 20px; border: 1px solid black;")


    def setCamera(self,camera):
        self.camera=camera

    def update(self):
        image = self.camera.getImage()[0]

        if image != None:
            imageTrans = self.camera.getImage()[1]
            img = QtGui.QImage(image.data, image.shape[1], image.shape[0], QtGui.QImage.Format_RGB888)
            scaledImage = img.scaled(self.imgLabel.size())
            self.imgLabel.setPixmap(QtGui.QPixmap.fromImage(scaledImage))
            img_trans = QtGui.QImage(imageTrans.data, imageTrans.shape[1], imageTrans.shape[0],QtGui.QImage.Format_Indexed8)
            img_trans2 = img_trans.convertToFormat(QtGui.QImage.Format_Indexed8)
            colortable = [QtGui.qRgb(i,i,i) for i in xrange(256)]
            img_trans.setColorTable(colortable)
            scaledTransImage = img_trans.scaled(self.transLabel.size())
            self.transLabel.setPixmap(QtGui.QPixmap.fromImage(scaledTransImage))
