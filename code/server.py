import socket
import threading
import time

PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
HEADER_LENGTH = 64
FORMAT = 'utf-8'
DISCONNECT = '!disconnect!'

#public IPs of python databases other than the localhost
knownServerIps = [
    '73.210.244.195'
]

#the domain of the python servers
knownServerDomains = [
    '1.1.2'
]

#Server Declarations
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((SERVER, PORT))

#For bigger server connections
serverQueries = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#handle clients after being connected in the start function
def handle_client(conn, addr):
    print(f"/n [NEW CONNECTION] {addr} connected")
    connected = True
    while connected:
        header = conn.recv(HEADER_LENGTH).decode(FORMAT)
        if header:
            header = int(header)
            msg = conn.recv(header).decode(FORMAT)
            if msg == DISCONNECT:
                connected = False
                break            
            if msg.startswith('1.1.1'):
                for x in range(0, 6):
                    msg.pop(0)
                searchThread = threading.Thread(target = searchPagesLocal, args = (msg))
                searchThread.start()
            print(f"[NEW MSG][BYTE LENGTH: {header}] {addr}: {msg}")
        else:
            continue
    print(f'[DISCONNECT] {addr} disconnected')

#custom recieving function so I can use the input as a search input 
def rcv(conn, addr):
    connected = True
    while connected:
        header = conn.recv(HEADER_LENGTH).decode(FORMAT)
        if header:
            header = int(header)
            msg = conn.recv(header)
            if msg == DISCONNECT:
                return False
            if msg.endswith('.1.1.1') and msg.startswith('0.'):
                for x in range(0, 7):
                    msg.pop(-1)
                SearchThread = threading.Thread(target = searchPagesLocal, args = (msg))
                SearchThread.start()
            if msg.startswith('1.'):
                searchString = ''
                for x in range(0, 7):
                    msg[-1] += searchString
                    msg.pop(-1)
                
                querySystems = False
                iterateNumber = 0
                for x in knownServerDomains:
                    if searchString == x:
                        querySystems = False
                        serverNumber = iterateNumber
                        break
                    else:
                        continue
                    iterateNumber += 1
                if querySystems:
                    SERVERCONN = knownServerIps[serverNumber]
                    PORTCONN = 2020
                    ADDR = (SERVERCONN, PORTCONN)
                    serverQueries.connect(ADDR)
                    queryThread = threading.Thread(target = queryMultiServer, args = (msg))
                    queryThread.start()
                else:
                    pass
            print(f'[NEW MSG][BYTE LENGTH: {header}] {addr}: {msg}')
        print(f'[DISCONNECT] {addr} diconnected')
            

#function for sending info to the client
def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER_LENGTH - len(send_length))
    server.send(send_length)
    server.send(message)

#function for quering the multi servers to get a file if the server doesn't have it
def queryMultiServer(msg):
    temServerIP = knowIP.server
    serverQuery.connect(())

#searching if the domain was made explicit
def searchPagesLocal(searchInput):
    file = 'contents/info/' + searchInput + '.txt'
    f = open(file, 'r')
    Atributes = []
    Keywords = []
    exec(f)
    sending = '192' + Atributes[1]
    send(sending)
    
#starting function
def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target = handle_client, args = (conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")

#console clearing for clarity
i = 0
while(i < 10):
    print(" ")
    i += 1
print("[STARTING]Starting Server...")

#calling the start function
start()