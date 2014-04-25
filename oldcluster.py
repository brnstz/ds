#!/usr/bin/env python

import pandas 
import  sklearn

from sklearn.cluster import MiniBatchKMeans, KMeans

#print "train df"
#train_df = read_csv("expanded_mxm_dataset_train.txt")
print "test df"
test_df = pandas.io.parsers.read_csv("expanded_mxm_dataset_test.txt")

#print "train df 0"
#train_df = train_df.fillna(0)
print "test df 0"
test_df = test_df.fillna(0)

kmeans = MiniBatchKMeans()

kmeans.fit_trans
