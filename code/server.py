import socket
import threading
import time

PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
HEADER_LENGTH = 64
FORMAT = 'utf-8'
DISCONNECT = '!disconnect!'

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

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
                searchThread = threading.Thread(target = searchPagesBasic, args = (msg))
                searchThread.start()
            print(f"[NEW MSG][BYTE LENGTH: {header}] {addr}: {msg}")


        else:
            continue
    print(f'[DISCONNECT] {addr} disconnected')

def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER_LENGTH - len(send_length))
    server.send(send_length)
    server.send(message)

def searchPagesBasic(searchInput):
    file = 'contents/' + searchInput + '.txt'
    f = open(file, 'r')
    Atributes = []
    Keywords = []
    exec(f)
    sending = '192' + Atributes[1]
    send(sending)

def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target = handle_client, args = (conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")

i = 0
while(i < 10):
    print(" ")
    i += 1
print("[STARTING]Starting Server...")
start()