import socket
import tkinter as tk

window = tk.Tk()

HEADER = 64
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT = '!disconnect!'
SERVER = '192.168.1.147'
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((SERVER, PORT))

def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)



def start():
    searchbar.pack()
    search.grid(row = 0, column = 0, columnspan = 4)
    searchButton.grid(row = 0, column = 4)
    
    screen.pack()
    window.mainloop()
    connected = True
    header = client.recv(HEADER).decode()
    while connected:
        header = client.recv(HEADER).decode()
        if header:
            header = int(header)
            fileName = client.recv(header).decode()
            if fileName:
                if fileName[0] == '1' and fileName[1] == '9' and fileName[2] == '2':
                    for x in range(0, 3):
                        fileName.pop(0)
                    parse(fileName)
            else:
                continue

def searchFunc():
    searchInput = search.get()
    if searchInput.endswith('.local') and searchInput.startswith('0.'):
        send(searchInput)
        file = recv()
        parse(file)
    elif searchInput.endswith('.local') and not(searchInput.startswith('0.')):
        send('0.' + searchInput)
    else:
        send('0.' + searchInput + '.local')

def recv():
    header = client.recv(HEADER).decode(FORMAT)
    if header:
        header = int(header)
        msg = client.recv(header).decode(FORMAT)
        return msg

# Functions for writing code for the program to read
def parse(file):
    parserTrue = False
    f = open(file, 'r')
    line = 1
    while parserTrue:
        if(f.readline(line) == ' '):
            continue
        elif(f.readline(line) == 'endProj'):
            break
        elif(f.readline(line)[0] == '/' and f.readline(line)[1] == '/'):
            continue
        else:
            exec(f.readline(line))
            line += 1
    f.close()

def closeFunc():
    send(DISCONNECT)
    window.destroy()

#tkinter code
#Searchbar
searchbar = tk.Frame()
searchbar.pack()
search = tk.Entry(
    master = searchbar,
)
search.grid(row = 0, column = 3, columnspan = 9)
searchButton = tk.Button(
    text = u'✓',
    master = searchbar,
    command = searchFunc
)
searchButton.grid(row = 0, column = 11)
close = tk.Button(
    text = u'✘',
    master = searchbar,
    command = closeFunc
)
close.grid(row = 0, column = 12)

#Screens
screen = tk.Frame()
screen.pack()

start()