import sys, Ice
from PyQt4 import QtGui
from gui.gui import Gui
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
    window = Gui(source)
    window.show()

    if source == 0:
        camera = Camera()
        window.setCamera(camera)

        t1 = ThreadCamera(camera)
        t1.start()

        t2 = ThreadGui(window)
        t2.start()

    else:
        video_file = properties.getProperty("Detection.VideoFile")
        window.update(video_file)

    sys.exit(app.exec_())
