
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
        self.setWindowTitle("Number Classifier")
        #self.imgLabel=QtGui.QLabel(self)
        self.resize(1000,600)
        self.move(150,50)
        #self.imgLabel.show()
        self.updGUI.connect(self.update)

        #Original Image Label
        self.imgLabel=QtGui.QLabel(self)
        self.imgLabel.resize(640,480)
        self.imgLabel.move(70,50)
        self.imgLabel.show()

        #Transform Image Label
        self.transLabel=QtGui.QLabel(self)
        self.transLabel.resize(200,200)
        self.transLabel.move(750,50)
        self.transLabel.show()

        self.numbers = []
        #Numbers labels 0 to 9
        lab0=QtGui.QLabel(self)
        lab0.resize(30,30)
        lab0.move(835,450)
        lab0.setText('0')
        lab0.setAlignment(QtCore.Qt.AlignCenter)
        lab0.setStyleSheet("background-color: #7FFFD4; color: #000; font-size: 20px; border: 1px solid black;")
        self.numbers.append(lab0)

        lab1=QtGui.QLabel(self)
        lab1.resize(30,30)
        lab1.move(750,300)
        lab1.setText('1')
        lab1.setAlignment(QtCore.Qt.AlignCenter)
        lab1.setStyleSheet("background-color: #7FFFD4; color: #000; font-size: 20px; border: 1px solid black;")
        self.numbers.append(lab1)

        lab2=QtGui.QLabel(self)
        lab2.resize(30,30)
        lab2.move(835,300)
        lab2.setText('2')
        lab2.setAlignment(QtCore.Qt.AlignCenter)
        lab2.setStyleSheet("background-color: #7FFFD4; color: #000; font-size: 20px; border: 1px solid black;")
        self.numbers.append(lab2)

        lab3=QtGui.QLabel(self)
        lab3.resize(30,30)
        lab3.move(920,300)
        lab3.setText('3')
        lab3.setAlignment(QtCore.Qt.AlignCenter)
        lab3.setStyleSheet("background-color: #7FFFD4; color: #000; font-size: 20px; border: 1px solid black;")
        self.numbers.append(lab3)

        lab4=QtGui.QLabel(self)
        lab4.resize(30,30)
        lab4.move(750,350)
        lab4.setText('4')
        lab4.setAlignment(QtCore.Qt.AlignCenter)
        lab4.setStyleSheet("background-color: #7FFFD4; color: #000; font-size: 20px; border: 1px solid black;")
        self.numbers.append(lab4)

        lab5=QtGui.QLabel(self)
        lab5.resize(30,30)
        lab5.move(835,350)
        lab5.setText('5')
        lab5.setAlignment(QtCore.Qt.AlignCenter)
        lab5.setStyleSheet("background-color: #7FFFD4; color: #000; font-size: 20px; border: 1px solid black;")
        self.numbers.append(lab5)

        lab6=QtGui.QLabel(self)
        lab6.resize(30,30)
        lab6.move(920,350)
        lab6.setText('6')
        lab6.setAlignment(QtCore.Qt.AlignCenter)
        lab6.setStyleSheet("background-color: #7FFFD4; color: #000; font-size: 20px; border: 1px solid black;")
        self.numbers.append(lab6)

        lab7=QtGui.QLabel(self)
        lab7.resize(30,30)
        lab7.move(750,400)
        lab7.setText('7')
        lab7.setAlignment(QtCore.Qt.AlignCenter)
        lab7.setStyleSheet("background-color: #7FFFD4; color: #000; font-size: 20px; border: 1px solid black;")
        self.numbers.append(lab7)

        lab8=QtGui.QLabel(self)
        lab8.resize(30,30)
        lab8.move(835,400)
        lab8.setText('8')
        lab8.setAlignment(QtCore.Qt.AlignCenter)
        lab8.setStyleSheet("background-color: #7FFFD4; color: #000; font-size: 20px; border: 1px solid black;")
        self.numbers.append(lab8)

        lab9=QtGui.QLabel(self)
        lab9.resize(30,30)
        lab9.move(920,400)
        lab9.setText('9')
        lab9.setAlignment(QtCore.Qt.AlignCenter)
        lab9.setStyleSheet("background-color: #7FFFD4; color: #000; font-size: 20px; border: 1px solid black;")
        self.numbers.append(lab9)


    def setCamera(self,camera):
        self.camera=camera

    def update(self): #This function update the GUI for every time the thread change
        image = self.camera.getImage()[0]
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
        net_out = self.camera.classification(imageTrans)
        self.lightON(net_out)

    def lightON(self,out): #This function turn on the light for the network output
        for number in self.numbers:
            number.setStyleSheet("background-color: #7FFFD4; color: #000; font-size: 20px; border: 1px solid black;")
        self.numbers[out].setStyleSheet("background-color: #FFFF00; color: #000; font-size: 20px; border: 1px solid black;")
