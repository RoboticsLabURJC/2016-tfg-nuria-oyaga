import sys
sys.path.insert(0, '/home/nuria/TFG/caffe/python')

import caffe
import lmdb
import cv2
import numpy as np

lmdb_env = lmdb.open('/home/nuria/TFG/data/lmdb_test/testTransformation2_lmdb')
lmdb_txn = lmdb_env.begin()
lmdb_cursor = lmdb_txn.cursor()
datum = caffe.proto.caffe_pb2.Datum()
n = 0
i = 0
nImage = 1
loop = 0

ftype = 'P2'

zero = 0
one = 0
two = 0
three = 0
four = 0
five = 0
six = 0
seven = 0
eight = 0
nine = 0

def toPGM(image,nImage):
    n = 0
    i = 0

    (width,height) = image.shape

    pgmfile=open('Mix/data' + str(nImage) + '.pgm', 'w')
    pgmfile.write("%s\n" % (ftype))
    pgmfile.write("%d %d\n" % (width,height))
    pgmfile.write("255\n")

    txtfile=open('Mix/data' + str(nImage) + '.txt', 'w')
    txtfile.write("%s\n" % (ftype))
    txtfile.write("%d %d\n" % (width,height))
    txtfile.write("255\n")


    while i < height:
        if n == width - 1:
            pgmfile.write("%s\n" % (image[i][n]))
            txtfile.write("%s\n" % (image[i][n]))
            i = i + 1
            n = 0
        elif image[i][n + 1] < 10:
            pgmfile.write("%s   " % (image[i][n]))
            txtfile.write("%s   " % (image[i][n]))
            n = n + 1
        elif image[i][n + 1] < 100:
            pgmfile.write("%s  " % (image[i][n]))
            txtfile.write("%s  " % (image[i][n]))
            n = n + 1
        else:
            pgmfile.write("%s " % (image[i][n]))
            txtfile.write("%s " % (image[i][n]))
            n = n + 1

    pgmfile.close()

for key, value in lmdb_cursor:

    datum.ParseFromString(value)
    label = datum.label
    data = caffe.io.datum_to_array(datum)

    if label == 0 and zero <= 3:
        zero = zero + 1
        toPGM(data[0],nImage)
        nImage = nImage + 1
    if label == 1 and one <= 3:
        one = one + 1
        toPGM(data[0],nImage)
        nImage = nImage + 1
    if label == 2 and two <= 3:
        two = two + 1
        toPGM(data[0],nImage)
        nImage = nImage + 1
    if label == 3 and three <= 3:
        three = three + 1
        toPGM(data[0],nImage)
        nImage = nImage + 1
    if label == 4 and four <= 3:
        four = four + 1
        toPGM(data[0],nImage)
        nImage = nImage + 1
    if label == 5 and five <= 3:
        five = five + 1
        toPGM(data[0],nImage)
        nImage = nImage + 1
    if label == 6 and six <= 3:
        six = six + 1
        toPGM(data[0],nImage)
        nImage = nImage + 1
    if label == 7 and seven <= 3:
        seven = seven + 1
        toPGM(data[0],nImage)
        nImage = nImage + 1
    if label == 8 and eight <= 3:
        eight = eight + 1
        toPGM(data[0],nImage)
        nImage = nImage + 1
    if label == 9 and nine <= 3:
        nine = nine + 1
        toPGM(data[0],nImage)
        nImage = nImage + 1
