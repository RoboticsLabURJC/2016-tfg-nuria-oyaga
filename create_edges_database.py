import sys
sys.path.insert(0, '/home/nuria/TFG/caffe/python')
import caffe
import lmdb
import cv2
import numpy as np


lmdb_env = lmdb.open('/home/nuria/TFG/caffe/examples/mnist/Basica/Databases/mnist_trainDef_lmdb')
lmdb_txn = lmdb_env.begin()
lmdb_cursor = lmdb_txn.cursor()
datum = caffe.proto.caffe_pb2.Datum()

item_id = -1
batch_size = 256


new_lmdb_env = lmdb.open('/home/nuria/TFG/caffe/examples/mnist/Laplacian/Databases/mnist_trainDef_lmdb',map_size=int(1e12))
new_lmdb_txn = new_lmdb_env.begin(write=True)
new_lmdb_cursor = new_lmdb_txn.cursor()
new_datum = caffe.proto.caffe_pb2.Datum()


for key, value in lmdb_cursor:
    item_id = item_id + 1

    datum.ParseFromString(value)
    label = datum.label
    data = caffe.io.datum_to_array(datum) #shape (1,28,28)

    data_filter = cv2.Laplacian(data[0],-1,5) #shape (28,28)
    data_filter = cv2.convertScaleAbs(data_filter)
    data_filter = data_filter[np.newaxis,:, :] #dimensions to (1,28,28)

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
