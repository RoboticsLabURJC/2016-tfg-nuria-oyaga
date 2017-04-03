
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
        self.setWindowTitle("Detection")
        #self.imgLabel=QtGui.QLabel(self)
        self.resize(850,600)
        self.move(150,50)
        #self.imgLabel.show()
        self.updGUI.connect(self.update)

        #Original Image Label
        self.imgLabel=QtGui.QLabel(self)
        self.imgLabel.resize(700,500)
        self.imgLabel.move(70,50)
        self.imgLabel.show()



    def setCamera(self,camera):
        self.camera=camera

    def update(self): #This function update the GUI for every time the thread change
        image = self.camera.getImage()
        img = QtGui.QImage(image.data, image.shape[1], image.shape[0], QtGui.QImage.Format_RGB888)
        scaledImage = img.scaled(self.imgLabel.size())
        self.imgLabel.setPixmap(QtGui.QPixmap.fromImage(scaledImage))
