#!/usr/bin/env python3


from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import numpy as np
import inspect
import PySimpleGUI as sg
import matplotlib
import sys
import os.path
import time

matplotlib.use("TkAgg")
from pprint import pprint

from svcounters import get_all_counters, get_all_values_for_counters, open_db, to_dictionary, create_db


"""
Demonstrates one way of embedding Matplotlib figures into a PySimpleGUI window.

Basic steps are:
 * Create a Canvas Element
 * Layout form
 * Display form (NON BLOCKING)
 * Draw plots onto convas
 * Display form (BLOCKING)
"""

def choices_manager(previous_status, clicked):
    if clicked in previous_status:
        idx = previous_status.index(clicked)
        previous_status.pop(idx)
    else:
        previous_status.append(clicked)
    return previous_status


def plot_counters(conn, counters):
    if conn:
        print('gettng counters', counters)
        for x in counters:
            values = get_all_values_for_counters(conn, x)
            p_x = [x for x, y in values.items()]
            p_y = [y for x, y in values.items()]
            plt.plot(p_x, p_y)

    plt.grid(True)
    plt.tick_params(axis='both', length=6, width=2, labelsize=6, labelrotation=90)
    plt.margins(0.2)
    plt.legend(counters)

    # values = get_all_values_for_counters(conn, counter)
    """
    print("values are:", end='')
    pprint(values)
    

    plt.figure(1)
    plt.subplot(211)
    
    for k,v in values.items():
        #plt.plot(i,v, color='green', marker='.', linestyle='solid', label=k)
        plt.plot(k,v,"bo")
        i = i + 1
    
    ts = [x for x,y in values.items()]
    vlus = [y for x,y in values.items()]
    plt.plot(ts,vlus)"""
    fig = plt.gcf()  # get the figure to show
    return fig

    

#  The magic function that makes it possible.... glues together tkinter and pyplot using Canvas Widget


def draw_figure(canvas, figure):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side="top", fill="both", expand=1)
    return figure_canvas_agg


def delete_figure_agg(figure_agg):
    figure_agg.get_tk_widget().forget()
    plt.close("all")

def select_db(db_file):
    conn = None
    counters_list = []
    if db_file:
        conn = open_db(db_file)
        if conn:
            counters_list = get_all_counters(conn)
    return conn, counters_list

def get_dir():
    layout = [
        [sg.Text("Please click the Browse button to find the snapshots directory")],
        [sg.FolderBrowse()],
        [sg.Submit(), sg.Cancel()]
    ]
    ans = None
    window = sg.Window("Get snapshots", layout)
    while True:
        event, values = window.read()
        #print(f"event is {event}")
        if event in [ None, sg.WIN_CLOSED,"Cancel"]:
            break
        if event == "Submit":
            ans = values["Browse"]
            break
    window.close()
    return ans

def getDB():
    layout = [
        [sg.Text("Please click the Browse button to find the database")],
        [sg.FileBrowse()],
        [sg.Submit(), sg.Cancel()]
    ]
    ans = None
    window = sg.Window("Get database", layout)
    while True:
        event, values = window.read()
        #print(f"event is {event}")
        if event in [ None, sg.WIN_CLOSED,"Cancel"]:
            break
        if event == "Submit":
            ans = values["Browse"]
            break
    window.close()
    return ans

def getDBUpdating():
    layout = [
        [sg.Text("Updating DB..."), [sg.Text("This may take up to a minute")]]
    ]
    ans = ""
    window = sg.Window("Get directory", layout)
    while True:
        event, values = window.read()
    return " "
    

def main():
    # -------------------------------- GUI Starts Here -------------------------------#
    # fig = your figure you want to display.  Assumption is that 'fig' holds the      #
    #       information to display.                                                   #
    # --------------------------------------------------------------------------------#

    # print(inspect.getsource(PyplotSimple))
    menu_def = [
        [
            "&File",
            ["Open s&vTechSupport  wip", 
             "Open &Snapshots directory", # Convert snapshorts fles to .db file
             "&Open Analyzer DB", # Open DB file
             "&Close Analyzer DB", # Close DB file
             "E&xit"],
        ],
        ["&Tools", ["Filter Zeros"],],
        ["&Help", "&About"],
    ]

    conn = None
    db_file = ''
    counters_list = []

    sg.theme("LightGreen")
    figure_w, figure_h = 650, 450
    # define the form layout
    col_listbox = [
        [
            sg.Listbox(
                values=counters_list,
                change_submits=True,
                size=(50, 26),
                key="-LISTBOX-",
            )
        ],
        [sg.Text(" " * 24), sg.Exit(size=(5, 2))],
    ]

    col_multiline = sg.Col([[sg.MLine(size=(20, 1), key="-MULTILINE-")]], visible=False)
    col_canvas = sg.Col([[sg.Canvas(key="-CANVAS-", size=(800,600))]])
    col_plot = sg.Col(
        [
            [sg.Pane([col_canvas, col_multiline])],
        ]
    )

    graphs_tab = [
        [sg.Col(col_listbox), col_plot],
    ]


    messages_tab = []

    layout = [
        [sg.Menu(menu_def, )],      
        [
            sg.TabGroup(
                [
                    [
                        sg.Tab("Graphs", graphs_tab, tooltip="See your graph here"),
                        sg.Tab("Messages", messages_tab, tooltip="See important messages here"),
                    ]
                ]
            )
        ]
    ]
    # create the form and show it without the plot
    window = sg.Window(
        "svCounters Analyzer",
        layout,
        #size = (900,600),
        resizable=True,
        finalize=True,
    )

    canvas_elem = window["-CANVAS-"]
    multiline_elem = window["-MULTILINE-"]
    figure_agg = None
    choices = list()
    while True:

        if db_file == "":
            #conn, db_file, counters_lst = select_db()
            pass

        event, values = window.read()

        if event in (sg.WIN_CLOSED, "Exit"):
            break

        elif event == "About":
            window.disappear()
            sg.popup('About this program', 'Version 1.0',
                     'PySimpleGUI Version', sg.version,  grab_anywhere=True)
            window.reappear()
        elif event == "Open Analyzer DB":
            #db_file = getDB()
            db_file = sg.popup_get_file('Select analyzer DB file', file_types=(("ALL Files", "*.db"),))
            if db_file and len(db_file)>0:
                conn, counters_lst = select_db(db_file)
                choices = list()
                if conn:
                    print(f'Counters list len:{len(counters_lst)}')
                    window["-LISTBOX-"].Update(values=counters_lst)
                    # print(window["-LISTBOX-"][0])
        elif event == "Open Snapshots directory":
            #snapshots_dir = get_dir()
            snapshots_dir = sg.popup_get_folder('Select snapshots folder')
            if snapshots_dir and len(snapshots_dir)>0:
                db_file = os.path.join(snapshots_dir,"analyzer.db")
                conn = create_db(db_file)
                t0 = time.time()
                sg.popup("Updating DB file. Wait until counters list is populated.",
                    title=None,
                    background_color=None,
                    text_color=None,
                    auto_close=False,
                    auto_close_duration=None,
                    non_blocking=True,
                    icon=None,
                    line_width=None,
                    font=None,
                    no_titlebar=True,
                    grab_anywhere=False,
                    keep_on_top=True,
                    location=(None, None))
                print("Updating DB file...")
                to_dictionary(snapshots_dir, conn)
                dt = int(time.time() - t0)
                print(f"Finished updating in {dt} seconds!")

                choices = list()
                if conn:
                    counters_lst = get_all_counters(conn)
                    print(f'Counters list len:{len(counters_lst)}')
                    window["-LISTBOX-"].Update(values=counters_lst)
                    # print(window["-LISTBOX-"][0])
        elif event == "-LISTBOX-":
            if figure_agg:
                # ** IMPORTANT ** Clean up previous drawing before drawing again
                delete_figure_agg(figure_agg)
            # get first listbox item chosen (returned as a list)

            # choice = values['-LISTBOX-'][0]
            # get function to call from the dictionary
            choice = ""
            if event == "-LISTBOX-":
                choice = values["-LISTBOX-"][0]
                print("Choice is {choice}")
            choices = choices_manager(choices, choice)
            # get values as dic from get_all_values_for_counters
            # pass the dict to PyplotFormatstr() to plot the graph
            fig = plot_counters(conn, choices)
            figure_agg = draw_figure(window["-CANVAS-"].TKCanvas, fig)  # draw the figure

        else: # unknown events
            print("Unhandled event: ", end='')
            pprint(event)
            print("values: ", end='')
            pprint(values)


if __name__ == "__main__":
    main()

