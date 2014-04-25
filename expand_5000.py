#!/usr/bin/env python

#from pandas.io.parsers import read_csv

import sys
import string
import pprint

def convert(split_line):
    c = [""] * 5002
    c[0] = split_line[0]
    c[1] = split_line[1]

    l = len(split_line)
    for i in range(2, len(split_line)):
        word_and_count = string.split(split_line[i], ":")
        word = word_and_count[0]
        count = word_and_count[1]
        index = int(word)
        c[index] = count

    return c

for line in sys.stdin:
    split_line = string.split(string.strip(line), ",")
    converted = convert(split_line)
    print ",".join(converted)

#test = read_csv("expand_test.txt")


