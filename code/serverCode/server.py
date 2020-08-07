from serverObject import server
import socket
import threading
import time

SERVER = socket.gethostbyname(socket.gethostname())

serverObject = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverObject.bind((SERVER, 5050))

knownIps = [

]

knownDomains = [

]

serverClass = server(serverObject, SERVER, knownIps, knownDomains)
serverClass.start()

# import socket
# import threading
# import time

# PORT = 5050
# SERVER = socket.gethostbyname(socket.gethostname())
# ADDR = (SERVER, PORT)
# HEADER_LENGTH = 64
# FORMAT = 'utf-8'
# DISCONNECT = '!disconnect!'

# #public IPs of python databases other than the localhost
# knownServerIps = [
#     '73.210.244.195'
# ]

# #the domain of the python servers
# knownServerDomains = [
#     '1.1.2'
# ]

# #Server Declarations
# server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# server.bind((SERVER, PORT))

# #For bigger server connections
# serverQueries = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# #Just some simple functions to make writng code easy
# def objectify(str):
#     return [char for char in str] 

# def deleteStrs(str, *args, **kwargs):
#     fromStart = kwargs.get('start', None)
#     fromEnd = kwargs.get('end', None)
#     str = objectify(str)
#     for x in range(0, fromStart + 1):
#         str.pop(0)
#     for x in range(0, fromEnd + 1):
#         str.pop(-1)
#     returnString = ''
#     for letter in str:
#         returnString += letter
#     return returnString

# #custom recieving function so I can use the input as a search input 
# def rcv(conn, addr):
#     connected = True
#     while connected:
#         header = conn.recv(HEADER_LENGTH).decode(FORMAT)
#         if header:
#             header = int(header)
#             msg = conn.recv(header)
#             if msg == DISCONNECT:
#                 return False
#             if msg.startswith('0.'):
#                 msg = deleteStrs(msg, start = 2)
#             if msg.startswith('1.'):
#                 searchString = ''
#                 for x in range(0, 7):
#                     msg[-1] += searchString
#                     msg.pop(-1)
                
#                 querySystems = False
#                 iterateNumber = 0
#                 for x in knownServerDomains:
#                     if searchString == x:
#                         querySystems = False
#                         serverNumber = iterateNumber
#                         break
#                     else:
#                         continue
#                     iterateNumber += 1
#                 if querySystems:
#                     SERVERCONN = knownServerIps[serverNumber]
#                     PORTCONN = 2020
#                     ADDR = (SERVERCONN, PORTCONN)
#                     serverQueries.connect(ADDR)
#                     queryThread = threading.Thread(target = queryMultiServer, args = (msg))
#                     queryThread.start()
#                 else:
#                     pass
#             print(f'[NEW MSG][BYTE LENGTH: {header}] {addr}: {msg}')
#         print(f'[DISCONNECT] {addr} diconnected')
            

# #handle each client
# def handle_client(conn, addr):
#     print(f"/n [NEW CONNECTION] {addr} connected")
#     rcv(conn, addr)

# #function for sending info to the client
# def send(msg, serverName):
#     message = msg.encode(FORMAT)
#     msg_length = len(message)
#     send_length = str(msg_length).encode(FORMAT)
#     send_length += b' ' * (HEADER_LENGTH - len(send_length))
#     exec(serverName + '.send(send_length)')
#     exec(serverName + '.send(message)')

# #function for quering the multi servers to get a file if the server doesn't have it
# def queryMultiServer(msg):
#     for ips in knownServerIps:
#         tempServerIP = ips
#         serverQueries.connect((tempServerIP, PORT))
#         send(msg, 'serverQueries')
        
    
# #starting function
# def start():
#     server.listen()
#     print(f"[LISTENING] Server is listening on {SERVER}")
#     while True:
#         conn, addr = server.accept()
#         thread = threading.Thread(target = handle_client, args = (conn, addr))
#         thread.start()
#         print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")

# #console clearing for clarity
# i = 0
# while(i < 10):
#     print(" ")
#     i += 1
# print("[STARTING]Starting Server...")

# #calling the start function
# start()