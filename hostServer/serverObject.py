import socket
import threading 

class hostServers:
    def __init__(self, socketObject, ADDR, databaseDomains, databaseIPs):
        self.ADDR = ADDR
        self.server = socketObject
        self.databaseDomains = databaseDomains
        self.databaseIPs = databaseIPs
        self.DISCONNECT = '!disconnect!'
        self.FORMAT = 'utf-8'
        self.HEADER_LENGTH = 64
        self.BUFFER_SIZE = 4096

    def start(self):
        self.server.listen()
        online = True
        while online:
            conn, addr = self.server.accept()
            handleClientThread = threading.Thread(target = self.handle_client, args = (conn, addr))
            handleClientThread.start()
    
    def handle_client(self, conn, addr):
        connected = True
        while connected:
            header = conn.recv(self.HEADER_LENGTH).decode(self.FORMAT)
            if header:
                msg = conn.recv(header).decode(self.FORMAT)
                print(f'[RECV]|{addr}|{msg}')
                if msg.startswith('dQ:'):
                    found = False 
                    enumerator = 0
                    for i in self.databaseDomains:
                        if msg == i:
                            found = True
                            domainName = i
                            domainIndex = enumerator
                        enumerator += 1
                    if found:
                        self.send(self.databaseIPs[domainIndex], 'server')
                    else:
                        self.send(self.askAround(msg), 'server')
    
    def send(self, msg, serverName):
        message = msg.encode(self.FORMAT)
        msg_length = len(message)
        send_length = str(msg_length).encode(self.FORMAT)
        send_length += b' ' * (self.HEADER_LENGTH - len(send_length))
        exec('self.' + serverName + '.send(send_length)')
        exec('self.' + serverName + '.send(message)')

    def sendFile(self, file, serverName):
        self.send('FileInfo', serverName)
        f = open(file, 'r')
        enumerator = 0
        req = True
        while req:
            alreadyRead = """"""
            lineToSend = f.readline(enumerator)
            self.send(lineToSend, serverName)
            alreadyRead += lineToSend
            if alreadyRead == f.read():
                req = False 
            enumerator += 1
            
        

    
    def askAround(self, domain):
        enumerator = 0
        needed = True
        while needed:
            self.serverQuery = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.connectionAddr = self.databaseIPs[enumerator]
            self.serverQuery.bind((self.serverQuery, 5050))
            msg = 'Domain:' + domain
            self.send(msg, 'serverQuery')
            header = self.serverQuery.recv(self.HEADER_LENGTH).decode(self.FORMAT)
            if header:
                header = int(header)
                reqIp = ''
                reqIp = self.serverQuery.recv(header).decode(self.FORMAT)
                if reqIp.startsWith('ip:'):
                    needed = False
                else:
                    self.send('AskIps', 'serverQuery')
                    header = self.serverQuery.recv(self.HEADER_LENGTH).decode(self.FORMAT)
                    if header:
                        header = int(header)
                        self.serverQuery.recv(header).decode(self.FORMAT)
            enumerator += 1
        return reqIp
            

