import sys, traceback, Ice
import jderobot
import numpy as np
import threading
import cv2
import Image
sys.path.insert(0, '/home/nuria/TFG/caffe/python')
import caffe

ddepth = -1
kw = dict(ksize=3, scale=1, delta=0, borderType=cv2.BORDER_DEFAULT)

ic = Ice.initialize(sys.argv)
properties = ic.getProperties()
filterMode = properties.getProperty("Numberclassifier.Filter")


class Camera():

    def __init__(self):

        self.lock = threading.Lock()
        #Net parameters necesary
        model_file = '/home/nuria/TFG/caffe/examples/mnist/lenet.prototxt'
        if (filterMode == "0"):
            #Canny filter
            pretrained_file = '/home/nuria/TFG/caffe/examples/mnist/lenet_edges_iter_10000.caffemodel'
        else:
            #Laplacian filter
            pretrained_file = '/home/nuria/TFG/caffe/examples/mnist/lenet_sobeledges_iter_10000.caffemodel'
        self.net = caffe.Classifier(model_file, pretrained_file, image_dims=(28, 28), raw_scale=255)

        try:
            obj = ic.propertyToProxy("Numberclassifier.Camera.Proxy")
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
        #Focus the image
        img_crop = img[0:480, 80:560]
        #Grayscale image
        img_gray = cv2.cvtColor(img_crop, cv2.COLOR_BGR2GRAY)
        #Resize image
        resize = cv2.resize(img_gray,(28,28))
        #Gaussian filter
        img_filt = cv2.GaussianBlur(resize, (5, 5), 0)
        if (filterMode == "0"):
            #Canny filter
            v = np.median(img_filt)
            sigma = 0.33
            lower = int(max(0, (1.0 - sigma) * v))
            upper = int(min(255, (1.0 + sigma) * v))
            edges = cv2.Canny(img_filt, lower, upper)
        else:
            #Laplacian filter
            edges = cv2.Laplacian(img_filt,-1,5)
            edges = cv2.convertScaleAbs(edges)
        kernel = np.ones((5,5),np.uint8)
        dilation = cv2.dilate(edges,kernel,iterations = 1)
        #Negative
        #neg = 255-resize
        return dilation
        #return neg

    def detection(self, img): #Uses caffe to detect the number we are showing
        self.net.blobs['data'].reshape(1,1,28,28)
        self.net.blobs['data'].data[...]=img
        output = self.net.forward()
        digito = output['prob'].argmax()
        return digito
