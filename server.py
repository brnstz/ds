#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pandas
import os.path
import h5py
import pprint
import decimal
import numpy
import operator
from time import time
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from sklearn.cluster import MiniBatchKMeans, KMeans
import sys

LOCAL_ROOT="/mnt/msd/AdditionalFiles"
MSD_ROOT="/mnt/msd/data"
ANALYSIS_FIELDS=['danceability', 'mode', 'tempo', 'time_signature', 'loudness']
MODE_MAP=["minor", "major"]
#SKIP_COMMON_WORD_COUNT=10
TOP_COUNT=50

# Load reverse stem mapping
def load_reverse():
    revmap = {}
    fh = open(os.path.join(LOCAL_ROOT, "mxm_reverse_mapping.txt"))
    for line in fh:
        line = line.strip()
        x = line.split("<SEP>")
        revmap[x[0]] = x[1]

    fh.close()
    return revmap

UNSTEMMED=load_reverse()

def load_stopwords():
    stopwords = {}
    fh = open(os.path.join(LOCAL_ROOT, "stopwords.txt"))
    words_arr = fh.read().split(",")
    fh.close()
    for word in words_arr:
        stopwords[word.strip()] = True

    return stopwords

STOPWORDS=load_stopwords()

def distance(a, b):
    dist = 0
    for i in range(len(a)):
        dist += (a[i] - b[i])**2

    return abs(dist)

def get_trackinfo(trackid):
    start = time()
    ti = { 'track_id': trackid }
    myfile = os.path.join(MSD_ROOT, trackid[2], trackid[3], trackid[4], trackid + ".h5")
    f = h5py.File(myfile, 'r')
    opent = time()
    print "open: ", opent - start
   
    (ti['mode'], ti['tempo'], ti['time_signature'], ti['loudness']) = f['analysis/songs'][0, 'mode', 'tempo', 'time_signature', 'loudness']
    analysist = time()
    print "analysis: ", analysist - opent

    # Round tempo to nearest tenths
    ti['tempo'] = int(decimal.Decimal(int(round(ti['tempo'], -1))))

    ti['artist_terms'] = f['metadata/artist_terms'][0:]
    ti['artist_terms_freq'] = f['metadata/artist_terms_freq'][0:]
    ti['artist_terms_weight'] = f['metadata/artist_terms_weight'][0:]
    metadata1 = time()
    print "metadata1: ", metadata1 - analysist

    #md = f['metadata/songs'][0]
    #i = 0
    #for val in f['metadata/songs'][0]:
    #    if i == 9:
    #        ti['artist_name'] = val
    #    elif i == 14:
    #        ti['album_name'] = val
    #    elif i == 18:
    #        ti['song_name'] = val
    #    elif i > 18:
    #        break
        
    #    i += 1
    # FIXME: is this slow even without extracting?    
    md = f['metadata/songs'][0]
    #ti['artist_name'] = "Artist"
    #ti['album_name'] = "Album"
    #ti['song_name'] = "Song"

    ti['artist_name'] = md[9]
    ti['album_name'] = md[14]
    ti['song_name'] = md[18]
    metadata = time()
    print "metadata: ", metadata - metadata1

    f.close()

    stop = time()

    print 'close file: ', stop - metadata1
    print 'final: ', stop - start

    return ti



class ClusterWorker():
    def __init__(self, c, words, center):
        self.c = c
        self.words = words
        self.center = center

    def process(self, row):
        words_only = row[0:5000]

        ti = get_trackinfo(row["_track_id"])
        print "adding track: %s: '%s'" % (ti["artist_name"], ti["song_name"])

        distance_from_center = distance(self.center, words_only)

        # Create a "quick" version of track without all info
        quick_track = { 
            "track_id": row["_track_id"],
            "distance":  distance_from_center,
        }
      
        # Append track to our list
        self.c["tracks"].append(quick_track)

        # Accumulate count for each word used
        for i in range(5000):
            stemmed_word = self.words[i]
            word = UNSTEMMED[stemmed_word]
            if not STOPWORDS.get(stemmed_word, False) and not STOPWORDS.get(word, False):
                if words_only[i] > 0.0:
                    # Ensure count is initialized
                    self.c["word_scores"].setdefault(word, 0)
                    # Add to count our track's value for this word
                    self.c["word_scores"][word] += words_only[i]

        # Accumulate count for each descriptive term
        for i in range(len(ti["artist_terms"])):
            term = ti["artist_terms"][i]
            self.c["term_scores"].setdefault(term, 0)
            self.c["term_scores"][term] += ti["artist_terms_weight"][i]

        if ti["mode"] == 0:
            self.c["mode_scores"]["minor"] += 1
        else:
            self.c["mode_scores"]["major"] += 1

        self.c["tempos"].append(ti["tempo"])

        

#class MusicHandler(BaseHTTPRequestHandler):
class MusicHandler():
    def get_clusters():
        pass

    def get_track():
        pass

    def init_cluster(self, label, center):
        res = {
            "center": center,
            "label": label,
            "tracks": [],
            "word_scores": {},
            "term_scores": {},
            "mode_scores": {"major": 0, "minor": 0},
            "tempos": []
        }
        
        return res

    # Create a new version of clusters.json
    def post_clusters(self):
        # Load initial dataframe (df)
        df = pandas.io.parsers.read_csv(
            os.path.join(LOCAL_ROOT, "head1000tracks.csv")
        )

        # Save track id for later use
        trackid = df['track_id']

        # Drop non-word columns 
        df = df.drop('mxm_track_id', 1)
        df = df.drop('track_id', 1)

        # Fill blank values with 0.0
        df = df.fillna(0.0)

        # Run fit
        kmeans = MiniBatchKMeans(n_clusters=1)
        kmeans.fit(df)

        clusters = [None] * kmeans.n_clusters

        workers = [None] * kmeans.n_clusters
        for i in range(kmeans.n_clusters):
            clusters[i] = self.init_cluster(kmeans.labels_[i], kmeans.cluster_centers_[i])
            workers[i] = ClusterWorker(clusters[i], qs[i], df.columns, kmeans.cluster_centers_[i])


        # Put labels in df
        df["_label"] = kmeans.labels_
        df["_track_id"] = trackid

        track_count = 0
        for index, row in df.iterrows():
            print "track count:", track_count
            w = workers[row["_label"]]
            w.process(row)


        # Clean up for output
        for i in range(kmeans.n_clusters):
            c = clusters[i]
            c["top_words"] =  sorted(c["word_scores"].iteritems(), key=operator.itemgetter(1), reverse=True)[:TOP_COUNT]
            c["top_terms"] =  sorted(c["term_scores"].iteritems(), key=operator.itemgetter(1), reverse=True)[:TOP_COUNT]
            c.pop("word_scores", None)
            c.pop("term_scores", None)

            c["median_tempo"] = numpy.median(c["tempos"])
            c.pop("tempos")
       
        pprint.pprint(clusters)



    def do_GET(self):
        if self.path == '/clusters.json':
            self.get_clusters()

        elif self.path.endswith('track.json'):
            self.get_track()

    def do_POST(self):
        if self.path == '/clusters.json':
            self.post_clusters()


#server = HTTPServer(('', 8080), MusicHandler)
#server.serve_forever()
handler = MusicHandler()
handler.post_clusters()
