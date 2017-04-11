
# -*- coding: utf-8 -*-

from PyQt4 import QtGui
from PyQt4 import QtCore
import numpy
import sys, cv2
import time


class Gui(QtGui.QWidget):

    updGUI=QtCore.pyqtSignal()

    def __init__(self, source, parent=None):

        QtGui.QWidget.__init__(self, parent)

        self.setWindowTitle("Detection")

        self.resize(850,600)
        self.move(150,50)

        self.updGUI.connect(self.update)

        #Original Image Label
        self.imgLabel=QtGui.QLabel(self)
        self.imgLabel.resize(700,500)
        self.imgLabel.move(70,50)
        self.imgLabel.show()

        #Source
        self.source = source



    def setCamera(self,camera):
        self.camera=camera

    def update(self,video): #This function update the GUI for every time the thread change
        if self.source == 0:
            image = self.camera.getImage()
        else:
            cap = cv2.VideoCapture(video)
            rate=cap.get(cv2.cv.CV_CAP_PROP_FPS);
            while not cap.isOpened():
                cap = cv2.VideoCapture(video)
                cv2.waitKey(1000)
                print "Wait for the header"

            pos_frame = cap.get(cv2.cv.CV_CAP_PROP_POS_FRAMES)
            fps = cap.get(cv2.cv.CV_CAP_PROP_FPS)
            rate = 1/fps
            total_time = 0

            while True:
                if total_time > rate or pos_frame == 0:
                    total_time = 0
                    flag, frame = cap.read()
                    if flag:
                        # The frame is ready and already captured
                        time_start = time.time()
                        frame =cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)

                        img = QtGui.QImage(frame.data, frame.shape[1], frame.shape[0],frame.shape[1] * 3, QtGui.QImage.Format_RGB888)
                        scaledImage = img.scaled(self.imgLabel.size())
                        self.imgLabel.setPixmap(QtGui.QPixmap.fromImage(scaledImage))
                        pos_frame = cap.get(cv2.cv.CV_CAP_PROP_POS_FRAMES)
                        time_end = time.time()
                        total_time = time_end - time_start
                    else:
                        # The next frame is not ready, so we try to read it again
                        cap.set(cv2.cv.CV_CAP_PROP_POS_FRAMES, pos_frame-1)
                        print "frame is not ready"
                        # It is better to wait for a while for the next frame to be ready
                        cv2.waitKey(1000)

                    if cv2.waitKey(10) == 27:
                        break
                    if cap.get(cv2.cv.CV_CAP_PROP_POS_FRAMES) == cap.get(cv2.cv.CV_CAP_PROP_FRAME_COUNT):
                        # If the number of captured frames is equal to the total number of frames,
                        # we stop
                        break
                else:
                    time_start = time.time()
                    time.sleep(rate - total_time)
                    time_end = time.time()
                    total_time = total_time + (time_end - time_start)
