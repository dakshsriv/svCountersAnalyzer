#!/usr/bin/env python3


from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import numpy as np
import inspect
import PySimpleGUI as sg
import matplotlib

matplotlib.use("TkAgg")
from pprint import pprint

from svcountersanalyzer import get_all_counters, get_all_values_for_counters, open_db


"""
Demonstrates one way of embedding Matplotlib figures into a PySimpleGUI window.

Basic steps are:
 * Create a Canvas Element
 * Layout form
 * Display form (NON BLOCKING)
 * Draw plots onto convas
 * Display form (BLOCKING)
"""


def choicesManager(previous_status, clicked):
    if clicked in previous_status:
        idx = previous_status.index(clicked)
        previous_status.pop(idx)
    else:
        previous_status.append(clicked)
    return previous_status


def PyplotFormatstr(counters):
    conn = open_db()
    for x in counters:
        values = get_all_values_for_counters(conn, x)
        ts = [x for x, y in values.items()]
        vlus = [y for x, y in values.items()]
        plt.plot(ts, vlus)
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


# -------------------------------- GUI Starts Here -------------------------------#
# fig = your figure you want to display.  Assumption is that 'fig' holds the      #
#       information to display.                                                   #
# --------------------------------------------------------------------------------#

# print(inspect.getsource(PyplotSimple))

menu_def = [
    [
        "&File",
        ["&Open Browse      Ctrl-O", "&Save       Ctrl-S", "&Properties", "E&xit"],
    ],
    ["&Edit", ["&Paste", ["Special", "Normal",], "Undo"],],
    [
        "&Toolbar",
        ["---", "Command &1", "Command &2", "---", "Command &3", "Command &4"],
    ],
    ["&Help", "&About..."],
]

conn = open_db()
c = get_all_counters(conn)
counters_list = get_all_counters(conn)

sg.theme("LightGreen")
figure_w, figure_h = 650, 650
# define the form layout
col_listbox = [
    [
        sg.Listbox(
            values=counters_list,
            change_submits=True,
            size=(48, len(counters_list)),
            key="-LISTBOX-",
        )
    ],
    [sg.Text(" " * 24), sg.Exit(size=(5, 2))],
]

col_multiline = sg.Col([[sg.MLine(size=(70, 35), key="-MULTILINE-")]])
col_canvas = sg.Col([[sg.Canvas(size=(figure_w, figure_h), key="-CANVAS-")]])
col_instructions = sg.Col(
    [
        [sg.Pane([col_canvas, col_multiline], size=(800, 600))],
        [sg.Text("Grab square above and slide upwards to view source code for graph")],
    ]
)

graph_sector = [
    [sg.Text("Matplotlib Plot Test", font=("ANY 18"))],
    [sg.Col(col_listbox), col_instructions],
]

db_upload_assistance = []

layout = [
    [
        sg.TabGroup(
            [
                [
                    sg.Tab("Graph tab", graph_sector, tooltip="See your graph here"),
                    sg.Tab(
                        "DB Upload Assistance",
                        db_upload_assistance,
                        tooltip="This helps you get the counters, timestamps, and values ready.",
                    ),
                ]
            ]
        )
    ]
]
# create the form and show it without the plot
window = sg.Window(
    "Demo Application - Embedding Matplotlib In PySimpleGUI",
    layout,
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
