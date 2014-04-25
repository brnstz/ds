#!/usr/bin/env python

import pandas
import os.path
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

MSD_ROOT=/mnt/msd
LOCAL_ROOT="../data"

class MusicHandler(BaseHTTPRequestHandler):
    def get_clusters():
        pass

    def get_track():
        pass

    # Create a new version of clusters.json
    def post_clusters():
        # Load initial dataframe (df)
        df = pandas.io.parsers.read_csv(os.path.join(LOCAL_ROOT, "tracks.csv"))

        # Save track id for later use
        trackid = df['track_id']

        # Drop non-word columns 
        df = df.drop('mxm_track_id', 1)
        df = df.drop('track_id', 1)

        # Fill blank values with 0.0
        df = df.fillna(0.0)

        # Run fit
        kmeans = MiniBatchKMeans(n_clusters=50)
        kmeans.fit(df)


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
