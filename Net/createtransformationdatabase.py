import sys
sys.path.insert(0, '/home/nuria/TFG/caffe/python')
import random
import caffe
import lmdb
import cv2
import numpy as np
import math
import skimage

lmdb_env = lmdb.open('/home/nuria/TFG/caffe/examples/mnist/Original Net/Databases/mnist_test_lmdb')
lmdb_txn = lmdb_env.begin()
lmdb_cursor = lmdb_txn.cursor()
datum = caffe.proto.caffe_pb2.Datum()

item_id = -1
batch_size = 256


new_lmdb_env = lmdb.open('/home/nuria/TFG/caffe/examples/mnist/Transformation 0-6 Net/Databases/mnist_testTrans0-6_lmdb',map_size=int(1e12))
new_lmdb_txn = new_lmdb_env.begin(write=True)
new_lmdb_cursor = new_lmdb_txn.cursor()
new_datum = caffe.proto.caffe_pb2.Datum()


for key, value in lmdb_cursor:

    #item_id = item_id + 1
    datum.ParseFromString(value)
    label = datum.label
    data = caffe.io.datum_to_array(datum)

    """sobelx = cv2.Sobel(data[0],cv2.CV_64F,1,0,ksize=5)  # x
    sobely = cv2.Sobel(data[0],cv2.CV_64F,0,1,ksize=5)  # y

    edges = cv2.add(abs(sobelx),abs(sobely))

    edges = cv2.normalize(edges,None,0,255,cv2.NORM_MINMAX)
    edges = np.uint8(edges)

    data_filter = edges[np.newaxis,:, :]

    new_datum = caffe.io.array_to_datum(data_filter,label)
    keystr = '{:0>8d}'.format(item_id)
    new_lmdb_txn.put( keystr, new_datum.SerializeToString() )"""

    for i in range(6):
        item_id = item_id + 1
        #Scale
        size = random.uniform(0.5, 1.5)
        size = round(size,2)
        res = cv2.resize(data[0],None,fx=size, fy=size, interpolation =cv2.INTER_LINEAR)
        s = res.shape[0]
        if size>1:
            crop1 = (s-28)/2
            res = res[crop1:crop1+28,crop1:crop1+28]
        else:
            border = int(math.ceil((28.0-s)/2))
            res = cv2.copyMakeBorder(res,border,border,border,border,cv2.BORDER_CONSTANT,value=0)
            if res.shape[0] > 28:
                crop1 = (res.shape[0]-28)/2
                res = res[crop1:crop1+28,crop1:crop1+28]

        #Rotation
        rows,cols = res.shape
        angle = random.randint(-20, 20)
        M = cv2.getRotationMatrix2D((cols/2,rows/2),angle,1)
        rotate = cv2.warpAffine(res,M,(cols,rows))

        #Translation
        rows,cols = rotate.shape
        if size>1:
            M = np.float32([[1,0,random.randint(-2, 2)],[0,1,random.randint(-2, 1)]])
        else:
            M = np.float32([[1,0,random.randint(-4, 4)],[0,1,random.randint(-4, 2)]])
        transl = cv2.warpAffine(rotate,M,(cols,rows))

        #Noise
        noisy = skimage.util.random_noise(transl, mode='gaussian', seed=None, clip=True, var=0.02)

        #Sobel
        sobelx = cv2.Sobel(noisy,cv2.CV_64F,1,0,ksize=5)  # x
        sobely = cv2.Sobel(noisy,cv2.CV_64F,0,1,ksize=5)  # y

        edges = cv2.add(abs(sobelx),abs(sobely))

        edges = cv2.normalize(edges,None,0,255,cv2.NORM_MINMAX)
        edges = np.uint8(edges)

        data_filter = edges[np.newaxis,:, :]

        new_datum = caffe.io.array_to_datum(data_filter,label)

        keystr = '{:0>8d}'.format(item_id)
        new_lmdb_txn.put( keystr, new_datum.SerializeToString() )


    # write batch
    if(item_id + 1) % batch_size == 0:
        new_lmdb_txn.commit()
        new_lmdb_txn = new_lmdb_env.begin(write=True)
        print (item_id + 1)


# write last batch
if (item_id+1) % batch_size != 0:
    new_lmdb_txn.commit()
    print 'last batch'
    print (item_id + 1)
