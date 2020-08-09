import socket
import threading
import os
import string
import tkinter as tk

def objectify(str):
    return [char for char in str] 

def deleteStrs(str, *args, **kwargs):
    fromStart = kwargs.get('start', None)
    fromEnd = kwargs.get('end', None)
    str = objectify(str)
    if fromStart:
        for x in range(0, fromStart + 1):
            str.pop(0)
    if fromEnd:
        for x in range(0, fromEnd + 1):
            str.pop(-1)
    returnString = ''
    for letter in str:
        returnString += letter
    return returnString

def searchFor(searchObject, toSearch, *args, **kwargs):
    needIndex = kwargs.get('index', False)
    needFind = kwargs.get('isfound', True)
    if needIndex:
        needFind = False
    if needIndex:
        returnNumber = 0
        for item in toSearch:
            if item == searchObject:
                return returnNumber
            else:
                returnNumber += 1
    elif needFind:
        for item in toSearch:
            if item == searchObject:
                return True
        return False

class client:
    def __init__(self, knownDomains, knownIPs):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.knownDomains = knownDomains
        self.knownIPs = knownIPs
        self.SERVER = ''
        self.PORT = 5050
        self.HEADER = 1024
        self.BUFFER = 1024
        self.DISCONNECT = '!disconnect!'
        self.RECOGNITION = '!recognition!'
        self.FORMAT = 'utf-8'

    def start(self):
        self.window = tk.Tk()
        self.searchbarFrame = tk.Frame(
            master = self.window
        )
        self.searchbar = tk.Entry(
            master = self.searchbarFrame
        )
        self.searchConfirm = tk.Button(
            master = self.searchbarFrame,
            text = 'Search',
            command = self.search
        )

        self.searchbarFrame.pack()
        self.searchbar.grid(row = 0, column = 0, columnspan = 17)
        self.searchConfirm.grid(row = 0, column = 17, colummspan = 2)

    def search(self):
        searchInput = self.searchbar.get()
        if searchInput.startswith('local'):
            searchInput = str.translate('.', '/')
            try:
                f = open(searchInput, 'r')
                exec(f.read())
            except:
                pass

    def send(self, msg):
        message = msg.encode(self.FORMAT)
        message_length = len(message)
        send_length = str(message_length)
        send_length += b' ' * (self.HEADER - len(send_length))
        