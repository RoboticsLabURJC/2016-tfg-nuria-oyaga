import sys
sys.path.insert(0, '/home/nuria/TFG/caffe/python')
import caffe
import lmdb
import cv2
import numpy as np


lmdb_env = lmdb.open('/home/nuria/TFG/lmdb_test/mnist_test_lmdb')
lmdb_txn = lmdb_env.begin()
lmdb_cursor = lmdb_txn.cursor()
datum = caffe.proto.caffe_pb2.Datum()

item_id = -1
batch_size = 256


new_lmdb_env = lmdb.open('/home/nuria/TFG/lmdb_test/test_neg_lmdb',map_size=int(1e12))
new_lmdb_txn = new_lmdb_env.begin(write=True)
new_lmdb_cursor = new_lmdb_txn.cursor()
new_datum = caffe.proto.caffe_pb2.Datum()


for key, value in lmdb_cursor:
    item_id = item_id + 1

    datum.ParseFromString(value)
    label = datum.label
    data = caffe.io.datum_to_array(datum) #shape (1,28,28)

    new_datum = caffe.io.array_to_datum(data,label)

    keystr = '{:0>8d}'.format(item_id)
    new_lmdb_txn.put( keystr, new_datum.SerializeToString() )

    item_id = item_id + 1

    data_neg = 255-data

    new_datum = caffe.io.array_to_datum(data_neg,label)

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
