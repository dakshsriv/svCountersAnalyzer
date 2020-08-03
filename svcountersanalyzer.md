# SvCountersAnalyzer

## Step 1: Find each file

> ### a) Make a dictionary dct

> ### b) Open the directory ~/Projects/SvCountersAnalyser/snapshots/

> ### c) Loop through the folders, storing the  day with x

> ### d) Loop through the filenames, storing the hour with y

> ### e) Push to dct: Key:x,y and Value:{}

## Step 2: Find the word SVCLI

> ### a) For each key in dct:

>> ### i) Separate day from hour

>> ### ii) Change the day and hour to give the relative path to file

>> ### iii) Open file

>> ### iv) Save the lines between the lines "SVDIAG SVCLI: show interface inspection" and "SVDIAG SVCLI: show interface inspection load-balancer" individually in a list lst

>> ### v) give lst to dictionary with corresponding key

## Step 3: For each group under SVCLI, find key-value pairs

> ### a) For each key in dct:

>> ### i) Pull the value and store as lns

>> ### ii) Eliminate empty lines

>> ### iii) Find indexes of "=============" and store in a

>> ### iv) Dct = {}

>> ### dct2 = {}

>> ### vi)  Dct[value of index of ax-1 for ax in a] is dct2

>> ### iv) Dct = {}

>> ### dct2 = {}

>> ### vi)  Dct[value of index of ax-1 for ax in a] is dct2

## Step 4: Store in dictionary

# Complete

## Step 5: Store in sqlite db: /home/daksh/Projects/svCountersAnalyzer/analyze.db