#!/usr/bin/env python

import pandas
import os.path
import h5py
import pprint
import decimal
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from sklearn.cluster import MiniBatchKMeans, KMeans

LOCAL_ROOT="/mnt/msd/AdditionalFiles"
MSD_ROOT="/mnt/msd/data"
ANALYSIS_FIELDS=['danceability', 'mode', 'tempo', 'time_signature', 'loudness']
MODE_MAP=["minor", "major"]
SKIP_COMMON_WORD_COUNT=10
TOP_TERM_COUNT=20

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

        # Round tempo to nearest tenths
        ti['tempo'] = int(decimal.Decimal(int(round(ti['tempo'], -1))))

        ti['artist_terms'] = f['metadata/artist_terms'].value
        ti['artist_terms_freq'] = f['metadata/artist_terms_freq'].value
        ti['artist_terms_weight'] = f['metadata/artist_terms_weight'].value

        ti['artist_name'] = f['metadata/songs'][0][9]
        ti['album_name'] = f['metadata/songs'][0][14]
        ti['song_name'] = f['metadata/songs'][0][18]

        f.close()

        return ti

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
        kmeans = MiniBatchKMeans(n_clusters=10)
        kmeans.fit(df)

        # Res is a list of clusters.
        # Each cluster entry should look something like... work in progress
        # {
        #   "center": [1, 2, 3, 4],
        #   "tracks": ["trackids"...]
        #   "word_scores": [top 20 words that aren't in the most common],
        #   "sorted_terms": [top 20 terms by weight],
        #   "mode_count": {"major": 32324, "minor": 234},
        #   "median_tempo": 120,
        #   "median"
        # }
        #    
        res = {
            "words": df.columns,
            "clusters": [None] * len(kmeans.labels_)
            #"clusters": [self.init_cluster()] * len(kmeans.labels_),
        }
        for i in range(len(row["_label"])):
            res["clusters"][i] = self.init_cluster(kmeans.labels_[i], kmeans.cluster_centers_[i])

        # Put labels in df
        # 500
        df["_label"] = kmeans.labels_
        df["_track_id"] = trackid

        for index, row in df.iterrows():
            c = res["clusters"][row["_label"]]
            words_only = row[0:5000]

            ti = self.get_trackinfo(row["_track_id"])

            distance_from_center = distance(
                kmeans.cluster_centers_[row["_label"]], words_only
            )

            # Create a "quick" version of track without all info
            quick_track = { 
                "track_id": row["_track_id"],
                "distance":  distance_from_center,
            }
          
            # Append track to our list
            c["tracks"].append(quick_track)

            # Accumulate count for each word used
            for i in range(5000):
                word = df.columns[i]
                # Ensure count is initialized
                c["word_scores"].setdefault(word, 0)
                # Add to count our track's value for this word
                c["word_scores"][word] += words_only[i]

            # Accumulate count for each descriptive term
            for i in range(len(ti["artist_terms"])):
                term = ti["artist_terms"][i]
                c["term_scores"].setdefault(term, 0)
                c["term_scores"][term] += ti["artist_terms_weight"]

            if ti["mode"] == 0:
                c["mode_scores"]["minor"] += 1
            else:
                c["mode_scores"]["major"] += 1

            ti["tempos"] += ti["tempo"]

        pprint.pprint(res)



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
