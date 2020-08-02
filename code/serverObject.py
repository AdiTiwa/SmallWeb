import socket
import threading
import time

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

class server:
    def __init__(self, serverObject, ip, knownIPs, knownDomains, *args, **kwargs):
        self.server = serverObject
        self.querySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ip = ip
        self.databaseIPs = knownIPs
        self.databaseDomains = knownDomains
        self.MessageDatatbase = kwargs.get('MessageDatatbase', None)
        self.PORT = 5050
        self.HEADER = 64
        self.BUFFER = 64
        self.DISCONNECT = "!disconnect!"
        self.FORMAT = 'utf-8'
        self.fileToBeParsed = {
            'filename': '',
            'Domain': '',
            'update': 0
        }
    
    def handle_client(self, conn, addr):
        recvThread = threading.Thread(target = self.recv, args = (conn, addr))
        recvThread.start()
    
    def start(self):
        print(f"[LISTENING] Server is listening on {self.ip}")
        self.server.listen()
        connected = True
        while connected:
            conn, addr = self.server.accept()
            handleClientThread = threading.Thread(target = self.handle_client, args = (conn, addr))
            handleClientThread.start()
    
    def recv(self, conn, addr):
        connected = True
        while connected:
            header = self.server.recv(self.HEADER).decode(self.FORMAT)
            if header:
                header = int(header)
                msg = self.server.recv(header).decode(self.FORMAT)
                if msg.startswith('1.'):
                    self.fileToBeParsed['filename'] = deleteStrs(msg, start = 2)
                    self.fileToBeParsed['update'] += 1 
                elif msg.startswith('2.'):
                    self.fileToBeParsed['Domain'] = deleteStrs(msg, start = 2)
                    self.fileToBeParsed['update'] += 1
                if self.fileToBeParsed['update'] == 2:
                    sendFileThread = threading.Thread(target = self.fileSearchSend, args = (self.fileToBeParsed['filename'], self.fileToBeParsed['Domain']))
                    sendFileThread.start()
    
    def fileSearchSend(self, filename, domainSearch):
        for domain in self.databaseDomains:
            if domain == domainSearch:
                serverQuery = self.databaseIPs[searchFor(domain, self.databaseDomains)]
                self.querySocket.bind(serverQuery, self.PORT)
                self.send('FQ:' + filename, 'querySocket')
                response = self.rcv('querySocket')
                if response.startswith('F:'):
                    fileTxt = ""
                    while True:
                        file = ''
                        toAdd = self.rcv('querySocket')
                        if not(toAdd.startswith('fin')):
                            file += fileTxt
                        else:
                            break
                    self.sendBatch(self.sendTxtFile(fileTxt), 'server')

    def sendTxtFile(self, file):
        str = objectify(file)
        returnStrObject = []
        strToAppend = ''
        strTest = ''
        strTestLen = 0
        for letter in str:
            strToAppend += letter
            strTest = strToAppend.encode(self.FORMAT)
            strTestLen = len(strTest)
            if strTestLen == self.HEADER:
                returnStrObject.append(strToAppend)
        return returnStrObject

    def sendBatch(self, object, socketObject):
        for batch in object:
            exec('self.send(self.' + socketObject + ')')



    def rcv(self, serverObject):
        header = ''
        exec('header = self.' + serverObject + '.recv(self.HEADER).decode(self.FORMAT)')
        if header:
            header = int(header)
            msg = ''
            exec('msg = self.' + serverObject + '.recv(header).decode(self.FORMAT)')
            return msg
        else:
            pass
                

    def send(self, msg, serverObject):
        message = msg.encode(self.FORMAT)
        message_length = len(message)
        send_length = message_length.encode(self.FORMAT)
        send_length += b' ' * (self.HEADER - message_length)
        exec('self.' + serverObject + '.send(' + send_length + ')')
        exec('self.' + serverObject + '.send(' + message + ')')
