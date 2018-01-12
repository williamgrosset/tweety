#!/usr/bin/python
import socket
import ssl

'''
def create_http_header():
# GENERAL, REQUEST, then ENTITY
'''

def recv_timeout(socket):
    total_data = []
    while True:
        # Update 4096 to MAX_PACKET size?
        data = socket.recv(4096).decode('utf-8')
        if not data: break
        total_data.append(data)
    return ''.join(total_data)

def parse_resp(resp):
    # Remove empty items (from \r\n) from array
    return resp.split('\r\n')

def get_redirect_location(resp_arr):
    for string in resp_arr:
        if 'Location:' in string or 'location:' in string:
            return string[10:]

def requires_https(redirect_location):
    # Check in start of URL
    if 'https' in redirect_location:
        return True
    else:
        return False

'''
def get_status_code(resp_arr):
    string = resp_arr[0]
    # parse string for matching status code (regex)
'''

# TODO: parse URL from command-line arg(s)

# TODO: Loop and redirect until we get a 200 status code (break on error)
# Initially make an HTTP call following the 1.0 specification (TODO: header formatting)
# Loop and handle each status code appropriately (5xx, 404, 401, 302, 301, 200)
# Once we hit a 200, parse and save response

uw = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
uw.connect(('twitter.com', 80))

# Pull URL into host param
uw.send('GET / HTTP/1.0\r\nHost: twitter.com\r\n\r\n'.encode('utf-8'))
resp = recv_timeout(uw)
resp_array = parse_resp(resp)
redirect_location = get_redirect_location(resp_array)
print(resp_array)
print(redirect_location)

if requires_https(redirect_location):
    # Requires use to open and close the socket?
    uw = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s = ssl.wrap_socket(uw, ssl_version = ssl.PROTOCOL_TLS)
    s.connect(('twitter.com', 443))
    # Pull URL into host param (varies betweeen using www.)
    s.send('GET / HTTP/1.0\r\nHost: twitter.com\r\n\r\n'.encode('utf-8'))
    resp = recv_timeout(s)
    print(resp)
else:
    resp = recv_timeout(uw)
    print(resp)
    uw.close()
