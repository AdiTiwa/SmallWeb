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

    def start(self):
        self.server.listen()
        online = True
        while online:
            conn, addr = self.server.accept()
            handleClientThread = threading.Thread(target = self.handle_client, args = (conn, addr))
    
    def handle_client(self, conn, addr):
        connected = True
        while connected:
            header = conn.recv(self.HEADER_LENGTH).decode(self.FORMAT)
            if header:
                msg = conn.recv(header).decode(self.FORMAT)
                print(f'[RECV]|{addr}|{msg}')
                found = False 
                enumerator = 0
                for i in self.databaseDomains:
                    if msg == i:
                        found = True
                        domainName = i
                        domainIndex = enumerator
                    enumerator += 1
                if found:
                    self.send(self.databaseIPs[domainIndex])
                else:
                    self.askAround()
    
    def send(self, msg):
        message = msg.encode(self.FORMAT)
        msg_length = len(message)
        send_length = str(msg_length).encode(self.FORMAT)
        send_length += b' ' * (self.HEADER_LENGTH - len(send_length))
        self.server.send(send_length)
        self.server.send(message)
    
    def askAround(self, domain):
        while needed:
            self.serverQuery = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.connectionAddr = self.databaseIPs[]
            self.serverQuery.bind(())

