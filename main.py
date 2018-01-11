#!/usr/bin/python

import socket

# TODO: parse URL from command-line arg(s)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# TODO: error handling support for port
host_ip = socket.gethostbyname('www.github.com')
s.connect((host_ip, 80))

# TODO: getuseragent() from a python lib?
s.send('GET https://www.github.com/ HTTP/1.0\r\n\r\n'.encode('utf-8'))

# TODO: If 302 and http(s), wrap socket in a SSL



resp = s.recv(4096)
print(resp)

s.close()
