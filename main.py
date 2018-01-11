#!/usr/bin/python
import socket
import ssl

# TODO: parse URL from command-line arg(s)
host_ip = socket.gethostbyname('www.facebook.com')

# Initialize socket, wrap in SSL, and connect to host ip
uw = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s = ssl.wrap_socket(uw, ssl_version=ssl.PROTOCOL_TLS)
s.connect((host_ip, 443))

# Connect socket and send request
s.send('GET https://www.facebook.com/unsupportedbrowser HTTP/1.0\r\n\r\n'.encode('utf-8'))

# TODO: getuseragent() from a python lib?
# TODO: If 302 and http(s), wrap socket in a SSL

# Receive response on socket
resp = s.recv(4096)
print(resp)

s.close()
