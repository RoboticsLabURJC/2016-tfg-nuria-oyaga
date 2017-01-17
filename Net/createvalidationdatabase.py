import sys
sys.path.insert(0, '/home/nuria/TFG/caffe/python')
import random
import caffe
import lmdb
import cv2
import numpy as np
import math

lmdb_env = lmdb.open('/home/nuria/TFG/caffe/examples/mnist/mnist_trainSobel_lmdb')
lmdb_txn = lmdb_env.begin()
lmdb_cursor = lmdb_txn.cursor()
datum = caffe.proto.caffe_pb2.Datum()

item_id = -1
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
batch_size = 256


new_lmdb_env = lmdb.open('/home/nuria/TFG/caffe/examples/mnist/mnist_trainSobelDef_lmdb',map_size=int(1e12))
new_lmdb_txn = new_lmdb_env.begin(write=True)
new_lmdb_cursor = new_lmdb_txn.cursor()
new_datum = caffe.proto.caffe_pb2.Datum()

new_lmdb_env2 = lmdb.open('/home/nuria/TFG/caffe/examples/mnist/mnist_validationSobel_lmdb',map_size=int(1e12))
new_lmdb_txn2 = new_lmdb_env2.begin(write=True)



for key, value in lmdb_cursor:

    datum.ParseFromString(value)
    label = datum.label
    data = caffe.io.datum_to_array(datum)
    item_id = item_id + 1

    new_datum = caffe.io.array_to_datum(data,label)
    keystr = '{:0>8d}'.format(item_id)

    if label == 0:
        zero = zero + 1
        if zero<4739:
            new_lmdb_txn.put( keystr, new_datum.SerializeToString() )
        else:
            new_lmdb_txn2.put( keystr, new_datum.SerializeToString() )
    elif label == 1:
        one = one + 1
        if one<5394:
            new_lmdb_txn.put( keystr, new_datum.SerializeToString() )
        else:
            new_lmdb_txn2.put( keystr, new_datum.SerializeToString() )
    elif label == 2:
        two = two + 1
        if two<4768:
            new_lmdb_txn.put( keystr, new_datum.SerializeToString() )
        else:
            new_lmdb_txn2.put( keystr, new_datum.SerializeToString() )
    elif label == 3:
        three = three + 1
        if three<4906:
            new_lmdb_txn.put( keystr, new_datum.SerializeToString() )
        else:
            new_lmdb_txn2.put( keystr, new_datum.SerializeToString() )
    elif label == 4:
        four = four + 1
        if four<4675:
            new_lmdb_txn.put( keystr, new_datum.SerializeToString() )
        else:
            new_lmdb_txn2.put( keystr, new_datum.SerializeToString() )
    elif label == 5:
        five = five + 1
        if five<4338:
            new_lmdb_txn.put( keystr, new_datum.SerializeToString() )
        else:
            new_lmdb_txn2.put( keystr, new_datum.SerializeToString() )
    elif label == 6:
        six = six + 1
        if six<4735:
            new_lmdb_txn.put( keystr, new_datum.SerializeToString() )
        else:
            new_lmdb_txn2.put( keystr, new_datum.SerializeToString() )
    elif label == 7:
        seven = seven + 1
        if seven<5013:
            new_lmdb_txn.put( keystr, new_datum.SerializeToString() )
        else:
            new_lmdb_txn2.put( keystr, new_datum.SerializeToString() )
    elif label == 8:
        eight = eight + 1
        if eight<4682:
            new_lmdb_txn.put( keystr, new_datum.SerializeToString() )
        else:
            new_lmdb_txn2.put( keystr, new_datum.SerializeToString() )
    else:
        nine = nine + 1
        if nine<4760:
            new_lmdb_txn.put( keystr, new_datum.SerializeToString() )
        else:
            new_lmdb_txn2.put( keystr, new_datum.SerializeToString() )

    # write batch
    if(item_id + 1) % batch_size == 0:
        new_lmdb_txn.commit()
        new_lmdb_txn = new_lmdb_env.begin(write=True)
        new_lmdb_txn2.commit()
        new_lmdb_txn2 = new_lmdb_env2.begin(write=True)
        print (item_id + 1)


# write last batch
if (item_id+1) % batch_size != 0:
    new_lmdb_txn.commit()
    new_lmdb_txn2.commit()
    print 'last batch'
    print (item_id + 1)
