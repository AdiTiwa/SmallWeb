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

class client:
    def __init__(self, conn, addr):
        self.conn = conn
        self.addr = addr
    def handle_client(self):
        print(f"/n [NEW CONNECTION] {self.addr} connected")

        connected = True
        while connected:
            header = self.conn.recv(HEADER_LENGTH).decode(FORMAT)
            if header:
                header = int(header)
                msg = self.conn.recv(header).decode(FORMAT)
                if msg == DISCONNECT:
                    connected = False
                    break            
                print(f"[NEW MSG][BYTE LENGTH: {header}] {self.addr}: {msg}")
            else:
                continue
        print(f'[DISCONNECT] {self.addr} disconnected')
    def send(self, msg):
        message = msg.encode(FORMAT)
        msg_length = len(message)
        send_length = str(msg_length).encode(FORMAT)
        send_length += b' ' * (HEADER_LENGTH - len(send_length))
        server.send(send_length)
        server.send(message)


def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, addr = server.accept()
        newClient = client(conn, addr)
        thread = threading.Thread(target = newClient.handle_client, args = (conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")

i = 0
while(i < 10):
    print(" ")
    i += 1
print("[STARTING]Starting Server...")
start()