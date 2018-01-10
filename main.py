#!/usr/bin/python

import socket

# TODO: parse URL from command-line arg(s)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# TODO: error handling support for port
s.connect(('www.google.com', 80))

s.send('GET / HTTP/1.0\n\n'.encode('utf-8'))
resp = s.recv(1024)
print(resp)

s.close()
