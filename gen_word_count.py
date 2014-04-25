#!/usr/bin/python

import sys

header = None

for line in sys.stdin:
    line = line.strip()
    params = line.split(",")
    if header == None:
        header = params
    else:
        for i in range(2, len(params)):
            try:
                count = int(params[i])
                for j in range(count):
                    print header[i]
            except:
                continue
