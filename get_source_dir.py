#!/usr/bin/python3

import PySimpleGUI as sg

def getdir():
    layout = [
        [sg.Text("Please click the Browse button to find the source directory")]
        ,
        [sg.FolderBrowse()]
        ,
        [sg.OK()]
    ]
    window = sg.Window("Get directory", layout)
    while True:
        event, values = window.read()
        if event == "OK":
            return(values["Browse"])

if __name__ == "__main__":
    getdir()