#!/usr/bin/python

import socket

s = socket.socket()
host = socket.gethostbyname('www.uvic.ca')
port = 8080

s.connect((host, port))
print(s.recv(1024))

s.close()
