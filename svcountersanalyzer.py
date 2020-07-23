#!/usr/bin/python3

from pprint import pprint
import os
import sys

def todictionary():
    dct = findEachFile()
    # pprint(dct)
    findTheWordSVCLI(dct)
    return ""

def findEachFile():
    dct = {}
    n = ""
    for root, dirs, files in os.walk( '/home/daksh/Projects/svCountersAnalyzer/snapshots', topdown=False):
        n = root
        for name in files:
            date = os.path.basename(root)
            hour = name.split('_')[1]
            v = "-".join([date, hour])
            vl = v[:-4]
            if vl not in dct:
                dct[vl] = dict()
            dct[vl]['time'] = vl
            dct[vl]['path'] = os.path.join(root, name)
    return dct

def findTheWordSVCLI(dct):
    interesting_line = False
    section_number = 0

    for d,info in dct.items():
        fname = info['path']
        print("PROCESSING FILE:", fname)
        with open( fname, 'r') as f:
            for l in f:
                line = l.strip() # now we have each line

                # New section starts or ends here
                if "SVDIAG" in line and interesting_line:
                    interesting_line = False
                    print("INTERESTING LINES END")
                    if section_number > 0:
                        sys.exit(1)

                # Processing intresting lines
                if interesting_line:
                    print( line)

                if "SVCLI" in line and "show interface inspection" in line:
                    interesting_line = True
                    section_number = section_number + 1
                    print("INTERESTING LINES START")
                    print( line)

    return ""

if __name__ == "__main__":
    print(todictionary())