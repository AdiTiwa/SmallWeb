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
        self.searchConfirm.grid(row = 0, column = 17, columnspan = 2)

        self.window.mainloop()

    def search(self):
        searchInput = self.searchbar.get()
        if searchInput.startswith('local'):
            searchInput = str.translate('.', '/')
            searchInput += '.txt'
            search = './' + searchInput
            try:
                exec(open(search).read(), {'self': self, 'tk': tk})
            except:
                exec(open('error.txt').read(), {'self': self, 'tk': tk})
        else:
            tempIp = ''
            for domain in self.knownDomains:
                if searchInput.startswith(domain):
                    tempIp = self.knownIPs[searchFor(domain, self.knownDomains, index = True)]
                    break
            if tempIp:
                addr = (tempIp, 5050)
                self.client.connect(addr)
                self.send('DQ. R')
                newMsg = self.recv()
                if newMsg == self.RECOGNITION:
                    self.send(searchInput, format = 'DQ.')
                    newMsg = self.recv()
                    if newMsg.startswith('F.'):
                        self.recvFile()
                    newMsg = self.recv()
                    if newMsg == 'Res.':
                        req = True
                        while req:
                            newMsg = self.recv()
                            if not newMsg == 'Res. E':
                                self.recvFile()
                            else:
                                req = False
                    filename = self.recv()
                    exec(f'toParse/{filename}')

    def recvFile(self):
        filename = deleteStrs(self.recv(), start = 2)
        filesize = deleteStrs(self.recv(), start = 2)
        with open(filename, 'wb') as f:
            needed = True
            while needed:
                bytesRead = self.recv()
                if not bytesRead:
                    needed = False
                    break
                f.write(bytesRead)

    def recv(self):
        header = self.client.recv(self.HEADER).decode(self.FORMAT)
        if header:
            header = int(header)
            msg = self.client.recv(header).decode(self.FORMAT)
            return msg

    def send(self, msg, *args, **kwargs):
        formatting = kwargs.get('format', '')
        msg = formatting + msg
        message = msg.encode(self.FORMAT)
        message_length = len(message)
        send_length = str(message_length)
        send_length += b' ' * (self.HEADER - len(send_length))
        self.client.send(send_length)
        self.client.send(message)
