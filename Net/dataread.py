import sys
sys.path.insert(0, '/home/nuria/TFG/caffe/python')

import caffe
import lmdb
import cv2
import numpy as np

lmdb_env = lmdb.open('/home/nuria/TFG/caffe/examples/mnist/Transformation 1-1 Net/Databases/mnist_validationTrans1-1_lmdb')
lmdb_txn = lmdb_env.begin()
lmdb_cursor = lmdb_txn.cursor()
datum = caffe.proto.caffe_pb2.Datum()
n = 0
i = 0
nImage = 1
loop = 0

ftype = 'P2'


for key, value in lmdb_cursor:

    n = 0
    i = 0

    if loop < 30:

        datum.ParseFromString(value)
        label = datum.label
        data = caffe.io.datum_to_array(datum)

        (width,height) = data[0].shape

        pgmfile=open('pruebas/data' + str(nImage) + '.pgm', 'w')
        pgmfile.write("%s\n" % (ftype))
        pgmfile.write("%d %d\n" % (width,height))
        pgmfile.write("255\n")

        txtfile=open('pruebas/data' + str(nImage) + '.txt', 'w')
        txtfile.write("%s\n" % (ftype))
        txtfile.write("%d %d\n" % (width,height))
        txtfile.write("255\n")

        nImage = nImage + 1
        loop = loop + 1

        while i < height:
            if n == width - 1:
                pgmfile.write("%s\n" % (data[0][i][n]))
                txtfile.write("%s\n" % (data[0][i][n]))
                i = i + 1
                n = 0
            elif data[0][i][n + 1] < 10:
                pgmfile.write("%s   " % (data[0][i][n]))
                txtfile.write("%s   " % (data[0][i][n]))
                n = n + 1
            elif data[0][i][n + 1] < 100:
                pgmfile.write("%s  " % (data[0][i][n]))
                txtfile.write("%s  " % (data[0][i][n]))
                n = n + 1
            else:
                pgmfile.write("%s " % (data[0][i][n]))
                txtfile.write("%s " % (data[0][i][n]))
                n = n + 1

        pgmfile.close()
