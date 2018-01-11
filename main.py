#!/usr/bin/python
import socket
import ssl

def recv_timeout(socket):
    total_data = []
    while True:
        data = socket.recv(4096)
        if not data: break
        total_data.append(data)
    return b''.join(total_data)

# TODO: parse URL from command-line arg(s)
host_ip = socket.gethostbyname('www.ubc.ca')

# TODO: Handle regular http (w/o SSL wrap)
# Initialize socket
# Sockt connection on port 80
# Hit http request (if we hit a 301 or 302 - target https support boolean flag)
# Wrap socket in a SSL
# Reinitialize socket connection (port 443) and send

# Initialize socket, wrap in SSL, and connect to host ip
uw = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s = ssl.wrap_socket(uw, ssl_version=ssl.PROTOCOL_TLS)
s.connect((host_ip, 443))

# Connect socket and send request
s.send('GET http://www.ubc.ca HTTP/1.0\r\n\r\n'.encode('utf-8'))

# TODO:
#   Header:
#   + getuseragent() from a python lib?

resp = recv_timeout(s)
print(resp)

s.close()
