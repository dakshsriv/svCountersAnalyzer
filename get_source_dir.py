#!/usr/bin/python3

import PySimpleGUI as sg

def getdir():
    layout = [
        [sg.Text("Please click the Browse button to find the source directory")]
        ,
        [sg.FolderBrowse()]
        ,
        [sg.Submit()]
    ]
    window = sg.Window("Get directory", layout)
    while True:
        event, values = window.read()
        if event == "Submit":
            return(values["Browse"])
            break

def getDB():
    layout = [
        [sg.Text("Please click the Browse button to find the database")]
        ,
        [sg.FileBrowse()]
        ,
        [sg.Submit()]
    ]
    window = sg.Window("Get directory", layout)
    while True:
        event, values = window.read()
        if event == "Submit":
            return(values["Browse"])
            break

if __name__ == "__main__":
    getDB()
    getdir()