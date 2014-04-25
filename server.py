#!/usr/bin/env python

import pandas
import os.path
import h5py
import pprint
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from sklearn.cluster import MiniBatchKMeans, KMeans

LOCAL_ROOT="/mnt/msd/AdditionalFiles"
MSD_ROOT="/mnt/msd/data"
ANALYSIS_FIELDS=['danceability', 'mode', 'tempo', 'time_signature', 'loudness']

def distance(a, b):
    dist = 0
    for i in range(len(a)):
        dist += (a[i] - b[i])**2

    return abs(dist)
        

#class MusicHandler(BaseHTTPRequestHandler):
class MusicHandler():
    def get_clusters():
        pass

    def get_track():
        pass

    def get_trackinfo(self, trackid):
        ti = { 'track_id': trackid }
        myfile = os.path.join(MSD_ROOT, trackid[2], trackid[3], trackid[4], trackid + ".h5")
        f = h5py.File(myfile, 'r')
        
        for field in ANALYSIS_FIELDS:
            ti[field] = f['analysis/songs'][field][0]

        ti['artist_terms'] = f['metadata/artist_terms'].value
        ti['artist_terms_freq'] = f['metadata/artist_terms_freq'].value
        ti['artist_terms_weight'] = f['metadata/artist_terms_weight'].value

        # Are these the correct indexes?
        ti['artist_name'] = f['metadata/songs'][0][9]
        ti['album_name'] = f['metadata/songs'][0][14]
        ti['song_name'] = f['metadata/songs'][0][18]

        f.close()

        return ti
        

    # Create a new version of clusters.json
    def post_clusters(self):
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
        # 500
        df["_label"] = kmeans.labels_
        df["_track_id"] = trackid

        for index, row in df.iterrows():
            words_only = row[0:5000]
            distance_from_center = distance(kmeans.cluster_centers_[row["_label"]], words_only)
            ti = self.get_trackinfo(row["_track_id"])
            ti["distance"] = distance_from_center
            pprint.pprint(ti)


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
