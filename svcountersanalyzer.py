#!/usr/bin/python3

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import matplotlib
from pprint import pprint
import os, sys, re, sqlite3, PySimpleGUI as sg
import numpy as np
import inspect
from get_source_dir import getdir
matplotlib.use('TkAgg')


def open_db( database = r"analyzer.db"):

    if not os.path.isfile(database):
        print("File not found")
        return None

    conn = None
    try:
        conn = sqlite3.connect(database)
        #print("Sqlite3 version", sqlite3.version)
    except exception as e:
        print("DB create error", e)
    return conn

def todictionary():
    dct = findEachFile()
    findTheWordSVCLI(dct)
    #pprint(dct)
    if os.path.isfile('./analyse.db'):
        os.remove("./analyse.db")
    conn = create_db()
    db_writer( conn, dct)
    sys.exit()
    #counters = get_all_counters( conn)
    # Display counters
    #counter = ""
    #get_all_values_for_counters( conn, counter)
    return ""

def db_writer( conn, dct):
    ctr = 0
    for timestamp,ctrs in dct.items():
        for counter_name,value in ctrs.items():
            insert_db(conn, counter_name, timestamp, value, "", "")
            ctr = ctr + 1
            print(ctr)

def findEachFile():
    dct = {}
    for root, dirs, files in os.walk( getdir(), topdown=False):
        for name in files:
            date = os.path.basename(root)
            print("date is {date}")
            hour = name.split('_')[1]
            v = "-".join([date, hour])
            vl = v[:-4]
            if vl not in dct:
                dct[vl] = dict()
            dct[vl]['path'] = os.path.join(root, name)
    return dct

def findTheWordSVCLI(dct):
    interesting_line = False     # Getting variables ready
    section_number = 0
    interesting_lst = list()
    # variable name = heading + countername + units
    previous_line = ""
    heading = ""
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
                        #print("heading:", heading)

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
                            if unit.isdigit():
                                unit2 = value
                                value = unit
                                unit = unit2
                            value = value.replace(",","")
                            if value.isdigit():
                                value = int(value)
                            k = "-".join([heading,counter,unit])
                            dct[d][k] = value
                    #print(">>>", line)

                if line.startswith("SVDIAG SVCLI") and "show interface inspection" in line:
                    interesting_line = True
                    cmd = line[7:]
                    #print("cmd:", cmd)
                    section_number = section_number + 1
                ctr = ctr + 1
                previous_line = line
        # Finding row values, column values, and sections
        #part_indexes = interesting_lst.index("============")
        
        #print(part_indexes)
        #pprint(interesting_lst)
    return dct

def create_db():
    database = r"analyzer.db"
    # create a database connection
    conn = None
    try:
        conn = sqlite3.connect(database)
        print("Sqlite3 version", sqlite3.version)
    except exception as e:
        print("DB create error", e)
    #finally:
    #    if conn:
    #        conn.close()

    sql_create_table = """ CREATE TABLE IF NOT EXISTS counters (
                                        counter text NOT NULL,
                                        timestamp text NOT NULL,
                                        value integer NOT NULL,
                                        type text,
                                        tags text
                                    ); """
    if conn is None:
        print("Error! cannot create the database connection.")
        return False

    try:
        c = conn.cursor()
        c.execute(sql_create_table)
    except Exception as e:
        print("Error executing SQL:", e)

    return conn

def insert_db(conn, counter_name, timestamp, value, c_type, tags):
    sql = ''' INSERT INTO counters(counter, timestamp, value, type, tags)
              VALUES(?,?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, (counter_name, timestamp, value, c_type, tags))
    conn.commit()

    return cur.lastrowid


def get_all_counters( conn):
    cur = conn.cursor()
    cur.execute("SELECT DISTINCT counter FROM counters")

    rows = cur.fetchall()
    counters = [ a for (a,) in rows if a not in ['time','path'] ]
    #pprint(counters)
    return counters

def get_all_values_for_counters( conn, counter):
    cur = conn.cursor()
    #print(f"counter is {counter}")
    cur.execute(f"SELECT * FROM counters WHERE counter='{counter}' ORDER BY timestamp")
    rows = cur.fetchall()
    values = dict()
    if len(rows)>0:
        values = { ts:value for (counter,ts, value,f_type,f_tags) in rows if counter not in ['time','path'] }
    return values



if __name__ == "__main__":
    #conn = create_db()
    #insert_db( conn, 'POLICY_ENGINE-OtherShunts-Unknown', '2020-04-23-03', 3382927, '', '')

    todictionary()

