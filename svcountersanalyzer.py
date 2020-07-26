#!/usr/bin/python3

from pprint import pprint
import os, sys, re

def todictionary():
    dct = findEachFile()
    findTheWordSVCLI(dct)
    pprint(dct)
    return ""

def findEachFile():
    dct = {}
    for root, dirs, files in os.walk( '/home/daksh/Projects/svCountersAnalyzer/snapshots', topdown=False):
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
    interesting_line = False     # Getting variables ready
    section_number = 0
    interesting_lst = list()
    for d,info in dct.items():
        fname = info['path']
        with open( fname, 'r') as f:    #Opening files
            for l in f:
                line = l.strip() # now we have each line

                # New section starts or ends here
                if "SVDIAG" in line and interesting_line:
                    interesting_line = False

                # Adding interesting line
                if interesting_line:
                    interesting_lst.append(line)       #Adding line
                    continue

                if line == "SVDIAG SVCLI: show interface inspection" and "show interface inspection" in line:
                    interesting_line = True
                    section_number = section_number + 1
        dct[d]=interesting_lst
        interesting_lst = list()
        # Finding row values, column values, and sections
        """ 
        Dct_structure : {"SVDIAG 
        SVCLI: show interface inspection":
        {<section nname i.e. IP CONTROL PATH>:
        {<row-column i.e. AdminShunts-Upstream(bytes)>:
                <value i.e. 0>}}}
        """
        #part_indexes = interesting_lst.index("============")
        
        #print(part_indexes)
        #pprint(interesting_lst)
    return dct

def findKeyValuePairs(dct):
    pass

if __name__ == "__main__":
    print(todictionary())