import sys, traceback, Ice
import jderobot
import numpy as np
import threading
import cv2
import Image

class Camera():

    def __init__(self):

        self.lock = threading.Lock()
        #Para probar problemas con transformada en el gui
        #cv2.namedWindow("Image",cv2.WINDOW_NORMAL)
        #cv2.resizeWindow("Image", 300, 300)

        try:
            ic = Ice.initialize()
            obj = ic.stringToProxy('cameraA:default -h localhost -p 9999')
            self.camera = jderobot.CameraPrx.checkedCast(obj)
            if self.camera:
                self.image = self.camera.getImageData("RGB8")
                self.height= self.image.description.height
                self.width = self.image.description.width
            else:
                print 'Interface camera not connected'

        except:
            traceback.print_exc()
            exit()
            status = 1

    def getImage(self):
        if self.camera:
            self.lock.acquire()
            image = np.zeros((self.height, self.width, 3), np.uint8)
            image = np.frombuffer(self.image.pixelData, dtype=np.uint8)
            image.shape = self.height, self.width, 3
            imageTrans = self.trasformImage(image)
            #imageTrans.shape = 28, 28, 1
            #Prueba para problemas con transformada
            #cv2.imshow('Image',imageTrans)
            images = [image,imageTrans]
            self.lock.release()
        return images

    def update(self):
        if self.camera:
            self.lock.acquire()
            self.image = self.camera.getImageData("RGB8")
            self.height= self.image.description.height
            self.width = self.image.description.width
            self.lock.release()

    def trasformImage(self, img):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        resize= cv2.resize(gray,(28,28))
        return resize
