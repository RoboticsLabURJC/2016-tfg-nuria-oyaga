import sys, traceback, Ice
import jderobot
import numpy as np
import threading
import cv2
import Image
sys.path.insert(0, '/home/nuria/TFG/caffe/python')
import caffe

class Camera():

    def __init__(self):

        self.lock = threading.Lock()

        #Net parameters necesary
        model_file = '/home/nuria/TFG/caffe/examples/mnist/lenet.prototxt'
        pretrained_file = '/home/nuria/TFG/caffe/examples/mnist/lenet_iter_10000.caffemodel'
        self.net = caffe.Classifier(model_file, pretrained_file, image_dims=(28, 28), raw_scale=255)

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

    def getImage(self): #This function gets the image from the webcam and trasformates it for the network
        if self.camera:
            self.lock.acquire()
            image = np.zeros((self.height, self.width, 3), np.uint8)
            image = np.frombuffer(self.image.pixelData, dtype=np.uint8)
            image.shape = self.height, self.width, 3
            imageTrans = self.trasformImage(image)
            images = [image,imageTrans]
            self.lock.release()
        return images

    def update(self): #Updates the camera every time the thread changes
        if self.camera:
            self.lock.acquire()
            self.image = self.camera.getImageData("RGB8")
            self.height= self.image.description.height
            self.width = self.image.description.width
            self.lock.release()

    def trasformImage(self, img): #Trasformates the image for the network
        crop_img = img[0:480, 80:560]
        gray = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)
        resize= cv2.resize(gray,(28,28))
        return resize

    def detection(self, img): #Uses caffe to detect the number we are showing
        self.net.blobs['data'].reshape(1,1,28,28)
        self.net.blobs['data'].data[...]=img
        output = self.net.forward()
        digito = output['prob'].argmax()
        return digito
