import sys
import numpy as np
import cv2
import Image
sys.path.insert(0, '/home/nuria/TFG/caffe/python')
import caffe
import lmdb

lmdb_env = lmdb.open('/home/nuria/TFG/lmdb_test/testTransformation_lmdb')

lmdb_txn = lmdb_env.begin()
lmdb_cursor = lmdb_txn.cursor()

datum = caffe.proto.caffe_pb2.Datum()

loop = 0

model_file = '/home/nuria/TFG/caffe/examples/mnist/lenet.prototxt'
pretrained_file = '/media/nuria/Seagate Expansion Drive/caffe/examples/mnist/Transformation 0-6 Net/lenet_iter_10000.caffemodel'
net = caffe.Classifier(model_file, pretrained_file, image_dims=(28, 28), raw_scale=255)

def classification(img): #Uses caffe to detect the number we are showing
    net.blobs['data'].reshape(1,1,28,28)
    net.blobs['data'].data[...]=img * 0.00390625
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
        net_out = classification(data)
        if label == net_out:
            conclusion = True
        else:
            conclusion = False
        testfile.write("Interacion " + str(loop) + ":")
        testfile.write(str(label) + " " + str(net_out) + " " + str(conclusion) + "\n")
        loop = loop + 1

        if loop % 1000 == 0:
            print (loop)
