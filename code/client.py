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
try:
    client.connect(ADDR)
except:
    print("There is an error, the server may not be online right now.")
    print("Run the server script on another ")

def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)

def start():
    #Searchbar
    searchbar = tk.Frame()
    searchbar.pack()
    search = tk.Entry(
        master = searchbar
    )
    search.grid(row = 0, column = 0, columnspan = 4)
    searchButton = tk.Button(
        text = u'✓',
        master = searchbar
    )
    searchButton.grid(row = 0, column = 4)

    #Screens
    screen = tk.Frame()
    screen.pack()

    window.mainloop()

start()