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
        model_file = '/home/nuria/TFG/caffe/examples/mnist/lenet.prototxt'
        pretrained_file = '/home/nuria/TFG/caffe/examples/mnist/Basica/lenet_iter_10000.caffemodel'
        self.net = caffe.Classifier(model_file, pretrained_file,
                    image_dims=(28, 28), raw_scale=255)

        status = 0

        ic = None
        # Initializing the Ice run-time.
        ic = Ice.initialize(sys.argv)
        properties = ic.getProperties()

        self.lock = threading.Lock()

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
        #Sobel filter
        sobelx = cv2.Sobel(img_filt,cv2.CV_64F,1,0,ksize=5)  # x
        sobely = cv2.Sobel(img_filt,cv2.CV_64F,0,1,ksize=5)  # y
        edges = cv2.add(abs(sobelx),abs(sobely))
        edges = cv2.normalize(edges,None,0,255,cv2.NORM_MINMAX)
        edges = np.uint8(edges)
        return edges

    def classification(self, img): #Uses caffe to class the number we are showing
        self.net.blobs['data'].reshape(1,1,28,28)
        self.net.blobs['data'].data[...]=img * 0.00390625
        output = self.net.forward()
        digito = output['prob'].argmax()
        return digito
