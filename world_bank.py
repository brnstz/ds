#!/usr/bin/env python

import pandas as pd

fh = open('output/world_bank.txt', 'w')

# Read in data 
df = pd.read_csv("world_bank.csv")

# Get unique set of indicators
indicators = set(df['Indicator_Name'])

# Find maximum value for each indicator
for indicator in indicators:
    subdf = df[df['Indicator_Name'] == indicator]
    max_idx = subdf['2011'].idxmax()
    max_country = subdf['Country_Name'][max_idx]
    max_value = subdf['2011'][max_idx]
    print >> fh, "%s has max value of %f for %s" % (max_country, max_value, indicator)

fh.close()
