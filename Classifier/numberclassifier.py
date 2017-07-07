import sys
from PyQt4 import QtGui
from gui.gui import Gui
from gui.threadgui import ThreadGui
from camera.camera import Camera
from camera.threadcamera import ThreadCamera
import signal

signal.signal(signal.SIGINT, signal.SIG_DFL)

if __name__ == '__main__':

    camera = Camera()
    print(camera)
    app = QtGui.QApplication(sys.argv)
    window = Gui()
    window.setCamera(camera)
    window.show()

    t1 = ThreadCamera(camera)
    t1.start()

    t2 = ThreadGui(window)
    t2.start()

    sys.exit(app.exec_())
