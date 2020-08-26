#!/usr/bin/python3

import PySimpleGUI as sg

def getdir():
    layout = [
        [sg.Text("Please click the Browse button to find the source directory")],
        [sg.FolderBrowse()],
        [sg.Submit()]
    ]
    window = sg.Window("Get directory", layout)
    while True:
        event, values = window.read()
        if event == "Submit":
            break
    ans = values["Browse"]
    return ans

def getDB():
    layout = [
        [sg.Text("Please click the Browse button to find the database")],
        [sg.FileBrowse()],
        [sg.Submit()]
    ]
    window = sg.Window("Get directory", layout)
    while True:
        event, values = window.read()
        if event == "Submit":
            break
    ans = values["Browse"]
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
        
if __name__ == "__main__":
    getDB()
    getdir()