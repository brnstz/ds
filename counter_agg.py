#!/usr/bin/env python

import pandas as pd

fh = open('output/nytimes_agg.csv', 'w')

# Read in data 
df = pd.read_csv("nytimes.csv")

# Group it
grouped = df.groupby(by=('Age', 'Gender', 'Signed_In'))

print >> fh, "age,gender,signed_in,avg_click,avg_impressions,max_click,max_impressions"
for name, group in grouped:
    # Start our output cols with our key (Age, Gender, Signed_In)
    output_cols = list(name)

    # Append our computed columns
    output_cols.append(group.Clicks.mean())
    output_cols.append(group.Impressions.mean())
    output_cols.append(group.Clicks.max())
    output_cols.append(group.Impressions.max())

    # Output to csv 
    print >> fh, ','.join(map(lambda x: str(x), output_cols))


fh.close()
