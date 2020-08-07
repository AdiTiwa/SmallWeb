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

def searchFor(searchObject, inObject):
    returnNumber = 0
    for object in inObject:
        if object == searchObject:
            return returnNumber
        else:
            returnNumber += 1
        return returnNumber

class client:
    def __init__(self, knownIps, knownDomains):
        self.knownIps = knownIps
        self.knownDomains = knownDomains
        self.HEADER = 1024
        self.BUFFER = 1024
        self.SERVER = socket.gethostbyname(socket.gethostname())
        self.PORT = 5050
        self.ADDR = (self.SERVER, self.PORT)
        self.FORMAT = 'utf-8'
        self.RECOGNITION = '!recognition!'
        self.DISCONNECT = '!disconnect!'
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect(self.ADDR)
        self.files = []
        self.init()

    def init(self):
        #first file check
        

        #tkinter code
        self.window = tk.Tk()
        #searchbar frame
        self.searchbar = tk.Frame(
            master = self.window
        )
        self.searchInputMain = tk.Entry(
            master = self.searchbar
        )
        self.searchConfirm = tk.Button(
            master = self.searchbar,
            text = u'✓',
        )
        self.endSession = tk.Button(
            master = self.searchbar,
            text = u'✘',
            comand = self.exitSession
        )
        self.screen = tk.Frame(
            master = self.window
        )
        self.searchbar.pack()
        self.searchInputMain.grid(row = 0, column = 0, columnspan = 17)
        self.searchConfirm.grid(row = 0, column = 17, columnspan = 2)
        self.endSession.grid(row = 0, column = 19)
        self.screen.pack()
        self.window.mainloop()

    def send(self, msg, *args, **kwargs):
        searchProtocol = kwargs.get('protocol', "")
        encoded = kwargs.get('encoded', False)
        if encoded and searchProtocol:
            msg = msg.decode(self.FORMAT)
            msg = searchProtocol + msg
            message = msg.encode(self.FORMAT)
        elif not(encoded) and searchProtocol:
            msg = searchProtocol + msg
            message = msg.encode(self.FORMAT)
        elif encoded and not(searchProtocol):
            message = msg
        else:
            message = msg.encode(self.FORMAT)
        msg_length = len(message)
        send_length  = str(msg_length).encode(self.FORMAT)
        send_length += b' ' * (self.HEADER - len(send_length))
        self.client.send(send_length)
        self.client.send(message)

    def search(self):
        searchInput = self.searchInputMain.get()
        if searchInput.endswith('local'):
            searchInput = str.translate('.', '/')
            searchInput += '.txt'
            res = {}
            f = open(searchInput, 'r')
            exec(f.read())
            

    def exitSession(self):
        self.send(self.DISCONNECT)
