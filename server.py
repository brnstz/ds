#!/usr/bin/env python

import pandas
import os.path
import h5py
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from sklearn.cluster import MiniBatchKMeans, KMeans

LOCAL_ROOT="/mnt/msd/AdditionalFiles"
MSD_ROOT="/mnt/msd/data"

def distance(a, b):
    dist = 0
    for i in range(len(a)):
    	dist += (a[i] - b[i])**2

    return abs(dist)
    
        

class MusicHandler(BaseHTTPRequestHandler):
    def get_clusters():
        pass

    def get_track():
        pass

	def get_trackinfo(trackid):
		ti = { "track_id": trackid }
		myfile = os.path.join(MSD_ROOT, trackid[2], trackid[3], trackid[4], trackid + ".h5")
		f = h5py.File(myfile, 'r')
		
		ti['danceability'] = f['analysis/songs']['danceability'] 
		ti['mode'] = f['analysis/songs']['danceability'] 
		
		

    # Create a new version of clusters.json
    def post_clusters():
        # Load initial dataframe (df)
        df = pandas.io.parsers.read_csv(os.path.join(LOCAL_ROOT, "head1000tracks.csv"))

        # Save track id for later use
        trackid = df['track_id']

        # Drop non-word columns 
        df = df.drop('mxm_track_id', 1)
        df = df.drop('track_id', 1)

        # Fill blank values with 0.0
        df = df.fillna(0.0)

        # Run fit
        kmeans = MiniBatchKMeans(n_clusters=10)
        kmeans.fit(df)

        # Put labels in df
        df["_label"] = kmeans.labels_
        df["_track_id"] = trackid


    def do_GET(self):
        if self.path == '/clusters.json':
            self.get_clusters()

        elif self.path.endswith('track.json'):
            self.get_track()

    def do_POST(self):
        if self.path == '/clusters.json':
            self.post_clusters()


server = HTTPServer(('', 8080), MusicHandler)
server.serve_forever()
