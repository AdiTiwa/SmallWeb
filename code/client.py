import socket
import tkinter as tk

window = tk.Tk()

HEADER = 64
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT = '!disconnect!'
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    client.connect(ADDR)
    
    #tkinter code
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
except:
    print("There is an error, and the server may not be online right now.")
    print("Run the server script on another computer on the same wifi.")
    print("It is recomended for you to run the server scripts on the ")
    print("command prompt->")
    print("Mac & Linux: python3 server.py")
    print("Windows: python server.py")

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




# Functions for writing code for the program to read
def parser(file):
    parserTrue = False
    f = open(file, 'r')
    line = 1
    while parserTrue:
        if(f.read(line) == ' '):
            continue
        elif(f.read(line) == 'endProj'):
            break
        elif(f.read(line)[0] == '/' and f.read(line)[1] == '/'):
            continue
        else:
            exec(f.read(line))
            line += 1



def label(msg, *args, **kwargs):
    fgColor = kwargs.get('fg', None)
    bgColor = kwargs.get('bg', None)
    width = kwargs.get('width', None)
    height = kwargs.get('height', None)
    newLabel = tk.Label(
        master = screen,
        text = msg,
        foreground = fgColor,
        background = bgColor,
        width = width,
        height = height
    )
    return newLabel

def button(text, *args, **kwargs):
    fgColor = kwargs.get('fg', None)
    bgColor = kwargs.get('bg', None)
    width = kwargs.get('width', None)
    height = kwargs.get('height', None)
    newButton = tk.Button(
        master = screen,
        text = text,
        fg = fgColor,
        bg = bgColor,
        width = width,
        height = height
    )
    return newButton

def img(src, Width, Height):
    canvas = tk.Canvas(
        master = screen,
        width = Width,
        height = Height
    )
    canvas.pack()
    img = tk.PhotoImage(file = src)
    canvas.create_image(
        0,
        0, 
        anchor = 'NW',
        image = img
    )

def commit(entry):
    entry.pack()

