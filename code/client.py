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

def objectify(str):
    return [char for char in str] 

def deleteStrs(str, *args, **kwargs):
    fromStart = kwargs.get('start', None)
    fromEnd = kwargs.get('end', None)
    str = objectify(str)
    for x in range(0, fromStart + 1):
        str.pop(0)
    for x in range(0, fromEnd + 1):
        str.pop(-1)
    returnString = ''
    for letter in str:
        returnString += letter
    return returnString

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
            

def searchFunc():
    searchInput = search.get()
    if searchInput.endswith('.local') and searchInput.startswith('0.'):
        searchInput = deleteStrs(searchInput, start = 2, end = 6)
        searchLocalURL(searchInput)
    elif searchInput.endswith('.local') and not(searchInput.startswith('0.')):
        searchInput = deleteStrs(searchInput, end = 6)
        searchLocalURL(searchInput)
    elif searchInput.startsWith('0.'):
        searchInput = deleteStrs(searchInput, start = 2)
        searchLocalURL(searchInput)
    else:
        pass

def recv():
    header = client.recv(HEADER).decode(FORMAT)
    if header:
        header = int(header)
        msg = client.recv(header).decode(FORMAT)
        return msg

def searchLocalURL(searchWord):
    searchWord = searchWord + '.txt'
    f = open('searchWord', 'r')
    Keywords = []
    Atributes = []
    exec(f.read())
    f.close()

def parse(file):
    f = open(file, 'r')
    exec(f.read())
    f.close()

# Functions for writing code for the program to read


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