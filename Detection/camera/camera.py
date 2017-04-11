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

        #Net parameters necesary
        #model_file = '/home/nuria/TFG/caffe/examples/mnist/lenet.prototxt'
        #pretrained_file = '/home/nuria/TFG/caffe/examples/mnist/Transformation 0-1 (Drop 0.5) Net/lenet_iter_7000.caffemodel'
        #self.net = caffe.Classifier(model_file, pretrained_file, image_dims=(28, 28), raw_scale=255)

        status = 0

        ic = None
        # Initializing the Ice run-time.
        ic = Ice.initialize(sys.argv)

        self.lock = threading.Lock()

        try:
            obj = ic.propertyToProxy("Detection.Camera.Proxy")
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
            self.lock.release()
        return image

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
        #Sobel filter
        sobelx = cv2.Sobel(img_filt,cv2.CV_64F,1,0,ksize=5)  # x
        sobely = cv2.Sobel(img_filt,cv2.CV_64F,0,1,ksize=5)  # y
        edges = cv2.add(abs(sobelx),abs(sobely))
        edges = cv2.normalize(edges,None,0,255,cv2.NORM_MINMAX)
        edges = np.uint8(edges)
        return edges
