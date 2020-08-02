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
    # variable name = heading + countername + units
    previous_line = ""
    heading = ""
    counter_name = ""
    cmd = ""
    tmp=[]
    units = list()
    for d,info in dct.items(): # for each file
        fname = info['path']
        with open( fname, 'r') as f:    #Opening files
            ctr = 0
            for l in f:
                line = l.strip() # now we have each line

                # New section starts or ends here
                if "SVDIAG" in line and interesting_line:
                    interesting_line = False
                    break

                # Adding interesting line
                if interesting_line:
                    if line.startswith("===="):
                        heading = previous_line.replace(" ","_")
                        print("heading:", heading)

                    elif line.startswith("----"):
                        units = previous_line.split()
                        units = units[1:]
                        if units[0].isalpha():
                            print("units:", units)
                    
                    elif len(line) < 10:
                        continue

                    else: # This is line has counter values
                        words = line.split()
                        counter = words[0]
                        for value,unit in zip(words[1:],units):
                            print(heading,counter,unit,value)
                            k = "-".join([heading,counter,unit])
                            dct[d][k] = value
                    print(">>>", line)

                if line.startswith("SVDIAG SVCLI") and "show interface inspection" in line:
                    interesting_line = True
                    cmd = line[7:]
                    print("cmd:", cmd)
                    section_number = section_number + 1
                ctr = ctr + 1
                previous_line = line
        # Finding row values, column values, and sections
        #part_indexes = interesting_lst.index("============")
        
        #print(part_indexes)
        #pprint(interesting_lst)
    return dct

def findKeyValuePairs(dct):
    pass

if __name__ == "__main__":
    print(todictionary())