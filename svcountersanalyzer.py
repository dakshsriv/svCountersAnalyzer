#!/usr/bin/python3

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import matplotlib
from pprint import pprint
import os, sys, re, sqlite3, PySimpleGUI as sg
import numpy as np
import inspect
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
    grapher( conn)
    sys.exit()
    db_writer( conn, dct)
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
    grapher( conn)

def grapher( conn):
    counters = get_all_counters( conn)
    counters_list = [v for (v,) in counters]
    fig_dict = {}
    for counter in counters:
        fig_dict[str(counter)] = counter
    sg.theme('LightGreen')
    figure_w, figure_h = 650, 650
    # define the form layout
    listbox_values = list(fig_dict)
    col_listbox = [[sg.Listbox(values=counters_list, change_submits=True, size=(50, len(listbox_values)), key='-LISTBOX-')],
                [sg.Text(' ' * 12), sg.Exit(size=(5, 2))]]

    col_multiline = sg.Col([[sg.MLine(size=(70, 35), key='-MULTILINE-')]])
    col_canvas = sg.Col([[sg.Canvas(size=(figure_w, figure_h), key='-CANVAS-')]])
    col_instructions = sg.Col([[sg.Pane([col_canvas, col_multiline], size=(800, 600))],
                            [sg.Text('Grab square above and slide upwards to view source code for graph')]])

    layout = [[sg.Text('Matplotlib Plot Test', font=('ANY 18'))],
            [sg.Col(col_listbox), col_instructions], ]

    # create the form and show it without the plot
    window = sg.Window('Demo Application - Embedding Matplotlib In PySimpleGUI',
                    layout, resizable=True, finalize=True)

    canvas_elem = window['-CANVAS-']
    multiline_elem = window['-MULTILINE-']
    figure_agg = None
    mkgraph( conn, counters[-1])
    while True:
        event, values = window.read()
        if event in (None, 'Exit'):
            break

        if figure_agg:
            # ** IMPORTANT ** Clean up previous drawing before drawing again
            delete_figure_agg(figure_agg)
        # get first listbox item chosen (returned as a list)
        choice = values['-LISTBOX-'][0]
        # get function to call from the dictionary
        func = fig_dict[choice]
        # show source code to function in multiline
        window['-MULTILINE-'].update(inspect.getsource(func))
        fig = func()                                    # call function to get the figure
        figure_agg = draw_figure(
            window['-CANVAS-'].TKCanvas, mkgraph(conn, counter[-1]))  # draw the figure

def PyplotSimple():
    import numpy as np
    import matplotlib.pyplot as plt

    names = ['group_a', 'group_b', 'group_c']
    values = [1, 10, 100]

    # evenly sampled time at 200ms intervals
    t = np.arange(0., 5., 0.2)

    # red dashes, blue squares and green triangles
    plt.plot(t, t, 'r--', t, t ** 2, 'bs', t, t ** 3, 'g^')

    fig = plt.gcf()  # get the figure to show
    return fig

def mkgraph( conn, counter):
    lv = get_all_values_for_counters( conn, "POLICY_ENGINE-OtherShunts-Upstream(pkts)")
    pprint(lv)
    names = ['group_a', 'group_b', 'group_c']
    values = [1, 10, 100]

    plt.figure(figsize=(9, 3))

    """plt.subplot(131)-                    
    plt.bar(names, values)"""
    """plt.subplot(132)
    plt.scatter(names, values)"""
    # Above four lines are for bar and scatter plots
    # Next two lines are for line graph
    plt.subplot(131)
    plt.plot(names, values)
    #plt.suptitle('Categorical Plotting')
    plt.show()



def delete_figure_agg(figure_agg):
    figure_agg.get_tk_widget().forget()
    plt.close('all')

def draw_figure(canvas, figure):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
    return figure_canvas_agg

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