import sys
import numpy as np
import cv2
import Image
sys.path.insert(0, '/home/nuria/TFG/caffe/python')
import caffe
import lmdb

lmdb_env = lmdb.open('/home/nuria/TFG/caffe/examples/mnist/Transformation 1-6 Net/Databases/mnist_validationTrans1-6_lmdb')
lmdb_txn = lmdb_env.begin()
lmdb_cursor = lmdb_txn.cursor()
datum = caffe.proto.caffe_pb2.Datum()

loop = 0

model_file = '/home/nuria/TFG/caffe/examples/mnist/lenet.prototxt'
pretrained_file = '/home/nuria/TFG/caffe/examples/mnist/Transformation 1-6 Net/lenet_iter_5500.caffemodel'
net = caffe.Classifier(model_file, pretrained_file, image_dims=(28, 28), raw_scale=255)

def detection(img): #Uses caffe to detect the number we are showing
    net.blobs['data'].reshape(1,1,28,28)
    net.blobs['data'].data[...]=img
    output = net.forward()
    digito = output['prob'].argmax()
    return digito

if __name__ == '__main__':

    testfile = open('caffenet_test.txt', 'w')
    testfile.write("El primer numero se corresponde con la etiqueta, el segundo con la salida de la red \n")

    for key, value in lmdb_cursor:
        datum.ParseFromString(value)
        label = datum.label
        data = caffe.io.datum_to_array(datum)
        net_out = detection(data[0])
        if label == net_out:
            conclusion = True
        else:
            conclusion = False
        testfile.write("Interacion " + str(loop) + ":")
        testfile.write(str(label) + " " + str(net_out) + " " + str(conclusion) + "\n")
        loop = loop + 1
