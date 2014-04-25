#!/usr/bin/env python

import sys
import pprint
import string

track = {}
for line in sys.stdin:
    sl= string.split(string.strip(line), "<SEP>")
    if len(sl) < 5:
        continue

    trackid = sl[0]
    track[trackid] = {
        "tid": sl[0],
        "artist_msd": sl[1],
        "artist_mxm": sl[4],
        "title_msd": sl[2],
        "title_mxm": sl[5]
    }

pprint.pprint(track)



