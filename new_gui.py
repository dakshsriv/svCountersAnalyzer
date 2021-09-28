#!/usr/bin/env python
#!/usr/bin/env python
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import numpy as np
import inspect
import PySimpleGUI as sg
import matplotlib
matplotlib.use('TkAgg')
from pprint import pprint


"""
Demonstrates one way of embedding Matplotlib figures into a PySimpleGUI window.

Basic steps are:
 * Create a Canvas Element
 * Layout form
 * Display form (NON BLOCKING)
 * Draw plots onto convas
 * Display form (BLOCKING)
"""




def PyplotFormatstr():

    def f(t):
        return np.exp(-t) * np.cos(2*np.pi*t)

    t1 = np.arange(0.0, 5.0, 0.1)
    t2 = np.arange(0.0, 5.0, 0.02)

    plt.figure(1)
    plt.subplot(211)
    plt.plot(t1, f(t1), 'bo', t2, f(t2), 'k')

    plt.subplot(212)
    plt.plot(t2, np.cos(2*np.pi*t2), 'r--')
    fig = plt.gcf()             # get the figure to show
    return fig


def draw_figure(canvas, figure):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
    return figure_canvas_agg


def delete_figure_agg(figure_agg):
    figure_agg.get_tk_widget().forget()
    plt.close('all')


# -------------------------------- GUI Starts Here -------------------------------#
# fig = your figure you want to display.  Assumption is that 'fig' holds the      #
#       information to display.                                                   #
# --------------------------------------------------------------------------------#

# print(inspect.getsource(PyplotSimple))


fig_dict = {'Pyplot Simple': PyplotFormatstr, 'Pyplot Formatstr': PyplotFormatstr, 'PyPlot Three': PyplotFormatstr,
            'Unicode Minus': PyplotFormatstr, 'Pyplot Scales': PyplotFormatstr, 'Axes Grid': PyplotFormatstr}


sg.theme('LightGreen')
figure_w, figure_h = 650, 650
# define the form layout
listbox_values = list(fig_dict)
col_listbox = [[sg.Listbox(values=listbox_values, change_submits=True, size=(28, len(listbox_values)), key='-LISTBOX-')],
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
    pprint(choice)
    func = fig_dict[choice]
    # show source code to function in multiline
    window['-MULTILINE-'].update(inspect.getsource(func))
    fig = func()                                    # call function to get the figure
    pprint (fig)
    figure_agg = draw_figure(
        window['-CANVAS-'].TKCanvas, fig)  # draw the figure
