import socket
import threading
import time
import os
import string

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

class server:
    def __init__(self, ip, knownIPs, knownDomains, domain, *args, **kwargs):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((ip, 5050))
        self.querySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ip = ip
        self.domain = domain
        self.databaseIPs = knownIPs
        self.databaseDomains = knownDomains
        self.MessageDatatbase = kwargs.get('MessageDatatbase', None)
        self.PORT = 5050
        self.HEADER = 1024
        self.BUFFER = 1024
        self.DISCONNECT = "!disconnect!"
        self.FORMAT = 'utf-8'
        self.recognition = '!recoognition!'
        self.domainQueriesIps = [

        ]
        self.domainQueriesPort = [

        ]
        self.fileDir = []
        self.files = []
    
    def handle_client(self, conn, addr):
        recvThread = threading.Thread(target = self.recv, args = (conn, addr))
        recvThread.start()
    
    def start(self):
        print(f"[LISTENING] Server is listening on {self.ip}")
        self.server.listen()
        connected = True
        reloadFilesThread = threading.Thread(target = self.reloadFiles)
        reloadFilesThread.start()
        while connected:
            conn, addr = self.server.accept()
            handleClientThread = threading.Thread(target = self.handle_client, args = (conn, addr))
            handleClientThread.start()
            

    def reloadFiles(self):
        for (dirpath, filenames) in os.walk('./contents'):
            for d in filenames:
                dirname = os.path.join(dirpath, d)
                if not(searchFor(dirname, self.files)) and not(dirname == ""):
                    self.files.append(d)
                    self.fileDir.append(dirname)

    
    def recv(self, conn, addr):
        connected = True
        while connected:
            header = self.server.recv(self.HEADER).decode(self.FORMAT)
            if header:
                header = int(header)
                msg = self.server.recv(header).decode(self.FORMAT)
                if msg.startswith('S.'):
                    pass
                elif msg.startswith('DQ. S'):
                    self.domainQueriesIps.append(addr)
                    self.domainQueriesPort.append(conn)
                elif msg.startswith('DQ. C'):
                    del self.domainQueriesIps[searchFor(addr, self.domainQueriesIps)]
                    del self.domainQueriesPort[searchFor(conn, self.domainQueriesPort)]
                    self.send(self.recognition, 'server')
    
    def fileSearch(self, search, domain):
        if self.domain == domain:
            filetranslate = str.maketrans('.', '/')
            filetranslate += '.txt'
            try:
                f = search.translate(filetranslate)
                if f.read():
                    try:
                        res = []
                        attr =[]
                        keys = []
                        exec(f.read())
                        if len(res) > 0:
                            self.send('Res.', 'server')
                        for file in res:
                            self.sendOtherFile(file, 'server')
                    except:
                        pass
            except:
                pass
        else:
            for ip in self.databaseIPs:
                if self.databaseDomains[searchFor(ip, self.databaseIPs, index = True)] == domain:
                    self.querySocket.connect((ip, 5050))
                    self.send('DQ S.', 'querySocket')
                    self.send(f'DQ F.{search}', 'querySocket')
    
    def recvFile(self, serverObject):
        f = ''
        exec(f'f = self.{serverObject}.recv(self.HEADER).decode(self.FORMAT)')
        if f == 'F.':
            filename = ''
            filesize = ''
            exec(f'filename = self.{serverObject}.recv(self.HEADER).decode(self.FORMAT)')
            exec(f"filesize = self.{serverObject}.recv(self.HEADER).decode(self.FORMAT)")
        else:
            return False
        

    def sendFile(self, fileLoc, serverObject):
        needed = True
        while needed:
            if fileLoc.endswith('.txt'):
                c = open(fileLoc, 'r')
                fileContents = c.read()
                fileContents = objectify(fileContents)
                returnString = ''
                returnArray = []
                for letter in fileContents:
                    if len(returnString.encode(self.FORMAT)) == self.HEADER:
                        returnArray.append(returnString.encode(self.FORMAT))
                        returnString = ''
                    else:
                        returnString += letter

                self.sendBatch(returnArray, serverObject, searchProtocol = 'FT.')
                needed = False
            else:
                self.sendOtherFile(fileLoc, 'server', searchProtocol = 'FO.')
                    
    def sendOtherFile(self, fileLoc, serverObject, *args, **kwargs):
        searchProtocol = kwargs.get('searchProtocol', '')
        filesize = os.path.getsize(fileLoc)
        exec(f"self.send('F.', serverObject)")
        exec('self.send(' + searchProtocol + fileLoc + ',' + serverObject + ')')
        exec(f'self.send({searchProtocol}, {filesize}, {serverObject})')

        with open(fileLoc, 'rb') as f:
            while True:
                bytesRead = f.read(self.BUFFER)
                if not(bytesRead > 0):
                    break
                exec(f"self.send({bytesRead}, {serverObject}, encoded = True)")
        
        exec(f"self.send('F. C', {serverObject})")
        

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

    def sendBatch(self, object, socketObject, *args, **kwargs):
        code = kwargs.get('searchProtocol', '')
        for batch in object:
            send = code.encode(self.FORMAT) + batch
            exec(f"self.send({send}, {socketObject}, encoded = True)")

    def rcv(self, *args, **kwargs):
        header = ''
        server = kwargs.get('serverObject', None)
        conn = kwargs.get('conn', None)
        if server:
            exec('header = self.' + server + '.recv(self.HEADER).decode(self.FORMAT)')
        elif conn:
            exec(f"header = {conn}.recv(self.HEADER).decode(self.FORMAT)")
        else:
            return False
        if header:
            header = int(header)
            msg = ''
            if server:
                exec('msg = self.' + server + '.recv(header).decode(self.FORMAT)')
            elif conn:
                exec(f"msg = {conn}.recv(header).decode(self.FORMAT)")
            return msg
        else:
            pass
                

    def send(self, msg, serverObject, *args, **kwargs):
        encoded = kwargs.get('encoded', False)
        code = kwargs.get('protocol', False)
        if encoded:
            if code:
                msg = code + msg
                message = msg.encode(self.FORMAT)
            else:
                message = msg.encode(self.FORMAT)
        message_length = len(message)
        send_length = message_length.encode(self.FORMAT)
        send_length += b' ' * (self.HEADER - message_length)
        exec('self.' + serverObject + '.send(' + send_length + ')')
        exec('self.' + serverObject + '.send(' + message + ')')
