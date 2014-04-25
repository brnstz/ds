#!/usr/bin/env python

execfile("./stem.py")
print "Loaded stem.py"
execfile("./track.py") 
print "Loaded track.py"
execfile("./word.py")
print "Loaded word.py"


#print len(STEM)
#print len(WORDS)
#print len(TRACKS)


import pandas
from sklearn.cluster import MiniBatchKMeans, KMeans
import pprint

#test_df = pandas.io.parsers.read_csv('../expanded_mxm_dataset_train.txt')
test_df = pandas.io.parsers.read_csv('../expanded_mxm_dataset_test.txt')

print "Loaded test_df"

ROWTRACK = test_df['track_id']
trackid = test_df['track_id']
test_df = test_df.drop('mxm_track_id', 1)
test_df = test_df.drop('track_id', 1)

test_df = test_df.fillna(0.0)
kmeans = MiniBatchKMeans(n_clusters=50)
kmeans.fit(test_df)
print "Finished fit"
test_df["ZZ_labels"] = kmeans.labels_
test_df['track_id'] = trackid
sorted_df = test_df.sort("ZZ_labels")

# FIXME
prev_label = None
#for label in kmeans.labels_:
for index, row in sorted_df.iterrows():
    label = row['ZZ_labels']
    if prev_label != label:
        print "label:", label
    pprint.pprint(TRACKS[row['track_id']])
    prev_label = label

print sorted_df.groupby('ZZ_labels').size()
print kmeans.inertia_


# kmeans.labels_ (has a entry for each row, each value
# 1-8 is the cluster the row belongs to)

# kmeans.cluster_centers_ is a list of 8 centroids

# create array of track names
# remove column
# 
