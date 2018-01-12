#!/usr/bin/python
import socket
import ssl

def recv_timeout(socket):
    total_data = []
    while True:
        # Update 4096 to MAX_PACKET size?
        data = socket.recv(4096).decode('utf-8')
        if not data: break
        total_data.append(data)
    return ''.join(total_data)

def parse_resp(resp):
    return resp.split('\r\n')

def find_redirect_location(resp_arr):
    for string in resp_arr:
        if 'Location:' in string:
            return string[10:]

def requires_https(redirect_location):
    # Check in start of URL
    if 'https' in redirect_location:
        return True
    else:
        return False

# TODO: parse URL from command-line arg(s)

uw = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
uw.connect(('facebook.com', 80))

uw.send('GET / HTTP/1.0\r\nHost: facebook.com\r\n\r\n'.encode('utf-8'))
resp = recv_timeout(uw)
resp_array = parse_resp(resp)
redirect_location = find_redirect_location(resp_array)
print(resp_array)
print(redirect_location)

# TODO: Loop and redirect until we get a 200 status code (break on error)

if requires_https(redirect_location):
    # Requires use to open and close the socket?
    uw = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s = ssl.wrap_socket(uw, ssl_version=ssl.PROTOCOL_TLS)
    s.connect(('facebook.com', 443))
    s.send('GET https://www.facebook.com/unsupportedbrowser HTTP/1.0\r\nHost: facebook.com\r\n\r\n'.encode('utf-8'))
    resp = recv_timeout(s)
    print(resp)
else:
    uw.close()
