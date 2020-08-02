#this is the code that will be running the master server for the client scripts

#this code is only for the code that is running on my own server. Thsi is recreateable for servers across the net
#email me at artkzo1111@gmail.com for trying to add your server to a discorverable server for all users
#other things: for adding you website to the readily avaliable for all users out of the box
import socket
import threading
import time
from serverObject import hostServers

hostServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
hostServer.bind((socket.gethostbyname(socket.gethostname()), 5050))

knownIps = [

]
knownDomains = [

]

server = hostServer(hostServer, socket.gethostbyname(socket.gethostname()), knownDomains, knownIps)
server.start()