#!/usr/bin/python3

# Traverse directory

import os
import os.path

for root, dirs, files in os.walk( '/home/daksh/Projects/svCountersAnalyzer/snapshots', topdown=False):
    for name in files:
        print(os.path.join(root, name))
        date = os.path.basename(root)
        hour = name.split('_')[1]
        hour = hour.split('.')[0]
        print( date, hour)

