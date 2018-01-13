#!/usr/bin/python
import socket
import ssl

def recv_timeout(socket):
    total_data = []
    while True:
        # Update 4096 to MAX_PACKET size?
        # issues with decoding? :/
        data = socket.recv(4096).decode('utf-8')
        if not data: break
        total_data.append(data)
    return ''.join(total_data)

def parse_response(response):
    # Remove empty items (from \r\n) from array
    return response.split('\r\n')

def get_redirect_location(resp_arr):
    for string in resp_arr:
        if 'Location:' in string or 'location:' in string:
            return string[10:]

def requires_https(redirect_location):
    # TODO: Check in start of URL
    if 'https' in redirect_location:
        return True
    else:
        return False

def send_request(socket, location, host):
    # TODO: Define HTTP 1.0 spec using BNF format (and pull into sep func)
    socket.send(('GET ' + location + ' HTTP/1.0\r\nHost: ' + host + '\r\n' + REQUEST_HEADER + '\r\n').encode('utf-8'))

'''
def create_http_header():
# GENERAL, REQUEST, then ENTITY
'''

'''
def get_status_code(resp_arr):
    string = resp_arr[0]
    # parse string for matching status code (regex)
'''

REQUEST_HEADER = 'From: williamhgrosset@gmail.com\r\n'

# TODO: parse URL from command-line arg(s)

# TODO: Loop and redirect until we get a 200 status code (break on error)
# Initially make an HTTP call following the 1.0 specification (TODO: header formatting)
# Loop and handle each status code appropriately (5xx, 404, 401, 302, 301, 200)
# Once we hit a 200, parse and save response

uw = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
uw.connect(('twitter.com', 80))

# Pull URL into host param
send_request(uw, '/', 'twitter.com')
resp = recv_timeout(uw)
resp_array = parse_response(resp)
redirect_location = get_redirect_location(resp_array)
print(resp_array)
print(redirect_location)

if requires_https(redirect_location):
    # Requires use to open and close the socket?
    uw = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s = ssl.wrap_socket(uw, ssl_version = ssl.PROTOCOL_TLS)
    s.connect(('twitter.com', 443))
    # Reference URL into host param (varies betweeen using www.)
    # Reference redirect_location in after GET method
    send_request(s, '/', 'twitter.com')
    resp = recv_timeout(s)
    print(resp)
else:
    resp = recv_timeout(uw)
    print(resp)
    uw.close()
