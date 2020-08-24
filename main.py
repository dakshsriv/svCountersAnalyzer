#!/usr/bin/env python3


from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import numpy as np
import inspect
import PySimpleGUI as sg
import matplotlib
import sys
from get_source_dir import getDB, getdir

matplotlib.use("TkAgg")
from pprint import pprint

from svcounters import get_all_counters, get_all_values_for_counters, open_db, todictionary


"""
Demonstrates one way of embedding Matplotlib figures into a PySimpleGUI window.

Basic steps are:
 * Create a Canvas Element
 * Layout form
 * Display form (NON BLOCKING)
 * Draw plots onto convas
 * Display form (BLOCKING)
"""
gdb = getDB()
conn = open_db(gdb)
tdb = todictionary(getdir(),gdb,conn)

def choicesManager(previous_status, clicked):
    if clicked in previous_status:
        idx = previous_status.index(clicked)
        previous_status.pop(idx)
    else:
        previous_status.append(clicked)
    return previous_status


def PyplotFormatstr(counters):
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

def main():
    # -------------------------------- GUI Starts Here -------------------------------#
    # fig = your figure you want to display.  Assumption is that 'fig' holds the      #
    #       information to display.                                                   #
    # --------------------------------------------------------------------------------#

    # print(inspect.getsource(PyplotSimple))

    menu_def = [
        [
            "&File",
            ["Open svTechSupport  wip    Ctrl-O", 
             "Open Snapshots             Ctrl-S", # Convert snapshorts fles to .db file
             "Open Analyzer &DB          Ctrl-D", # Open DB file
             "E&xit                               Ctrl-X"],
        ],
        ["&Tools", ["Filter Zeros"],],
        ["&Help", "&About..."],
    ]
    c = get_all_counters(conn)
    counters_list = get_all_counters(conn)

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
    choices = []
    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, "Exit"):
            break

        if figure_agg:
            # ** IMPORTANT ** Clean up previous drawing before drawing again
            delete_figure_agg(figure_agg)
        # get first listbox item chosen (returned as a list)
        """
        print("event: ", end='')
        pprint(event)
        print("values: ", end='')
        pprint(values)
        """
        # choice = values['-LISTBOX-'][0]
        # get function to call from the dictionary
        choice = values["-LISTBOX-"][0]
        choices = choicesManager(choices, choice)
        # get values as dic from get_all_values_for_counters
        # pass the dict to PyplotFormatstr() to plot the graph
        fig = PyplotFormatstr(choices)
        figure_agg = draw_figure(window["-CANVAS-"].TKCanvas, fig)  # draw the figure


if __name__ == "__main__":
    main()

