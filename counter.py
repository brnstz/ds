#!/usr/bin/python

import sys

# Init counters
total_age = 0
total_impressions = 0
total_clicks = 0
num_rows = 0

# Init tracking for oldest row
oldest_row = None
oldest_age = -sys.maxint - 1

out_fh = open('output/results.txt', 'w')

for line in sys.stdin:
    # Split into comma-separated pieces
    parts = line.strip().split(',')

    # Possible exception while running int() (e.g., header row, bad data)
    try:
        cur_age = int(parts[0])
        total_age += cur_age

        # Check for oldest row
        if cur_age > oldest_age:
            oldest_age = cur_age
            oldest_row = line

        total_impressions += int(parts[2])
        total_clicks += int(parts[3])

        num_rows += 1


    # Skip if non-int value found
    except:
        next


print >> out_fh, "Impressions Sum:", total_impressions
print >> out_fh, "Average Age:", total_age / num_rows
print >> out_fh, "Clickthrough Rate: ", "%.2f%%" % (100.0 * total_clicks/total_impressions) 
print >> out_fh, "Oldest Person:", oldest_row
out_fh.close()
