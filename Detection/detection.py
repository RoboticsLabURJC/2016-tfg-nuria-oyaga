import sys, Ice
from PyQt4 import QtGui
from gui.webcamgui import WebcamGui
from gui.videogui import VideoGui
from gui.threadgui import ThreadGui
from camera.camera import Camera
from camera.threadcamera import ThreadCamera
import signal

signal.signal(signal.SIGINT, signal.SIG_DFL)

if __name__ == '__main__':
    ic = Ice.initialize(sys.argv)
    properties = ic.getProperties()
    source = properties.getPropertyAsInt("Detection.Source")
    app = QtGui.QApplication(sys.argv)

    if source == 0:
        window = WebcamGui()
        camera = Camera()
        window.setCamera(camera)
        window.show()
        t1 = ThreadCamera(camera)
        t1.start()

        t2 = ThreadGui(window)
        t2.start()

    else:
        window = VideoGui()
        window.show()
        window.evaluate()


    sys.exit(app.exec_())
