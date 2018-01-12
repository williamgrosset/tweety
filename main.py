#!/usr/bin/python
import socket
import ssl

def recv_timeout(socket):
    total_data = []
    while True:
        # Update 4096?
        data = socket.recv(4096)
        if not data: break
        total_data.append(data)
    return b''.join(total_data)

def parse_resp(resp):
    return resp.decode().split('\r\n')

def find_redirect_location(resp_arr):
    for string in resp_arr:
        if 'Location:' in string:
            return string[10:]

def requires_https(redirect_location):
    if 'https' in redirect_location:
        return True
    else:
        return False

# TODO: parse URL from command-line arg(s)

uw = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
uw.connect(('amazon.com', 80))

uw.send('GET / HTTP/1.0\r\n\r\n'.encode('utf-8'))
resp = recv_timeout(uw)
resp_array = parse_resp(resp)
redirect_location = find_redirect_location(resp_array)
print(resp_array)
print(redirect_location)

# TODO: Loop and redirect until we get a 200 status code (break on error)

if requires_https(redirect_location):
    uw.close()
    uw = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s = ssl.wrap_socket(uw, ssl_version=ssl.PROTOCOL_TLS)
    s.connect(('amazon.com', 443))
    s.send('GET / HTTP/1.0\r\n\r\n'.encode('utf-8'))
    resp = recv_timeout(s)
    print(resp)
else:
    uw.close()
