#!/usr/bin/python
import socket
import ssl
import re

GENERAL_HEADER = ''
REQUEST_HEADER = 'From: williamhgrosset@gmail.com'
ENTITY_HEADER = ''

def recv_stream(socket):
    total_data = []
    while True:
        # Handle decoding error?
        data = socket.recv(8192).decode('utf-8')
        if not data: break
        total_data.append(data)
    return ''.join(total_data)

def parse_response(response):
    # TODO: Remove empty items from array
    return response.split('\r\n')

def get_redirect_location(response_array):
    for string in response_array:
        # TODO: Full regex of location: http(s)://domain.com/
        if 'Location:' in string or 'location:' in string:
            return string[10:]

def requires_https(redirect_location):
    # TODO: Check beginning of URL
    if 'https' in redirect_location: return True
    else: return False

def send_request(socket, location, host):
    # TODO: Define HTTP 1.0 spec using BNF format
    # TODO: Test with HTTP/2.0 servers
    socket.send(('GET ' + location + ' HTTP/1.0\r\nHost: ' + host + '\r\n' + REQUEST_HEADER + '\r\n\r\n').encode('utf-8'))

def get_status_code(status_line):
    status_code_match = re.match('HTTP\/\d\.\d (\d{3}).*', status_line)
    if status_code_match: return status_code_match.group(1)
    else: return 'No status code found.'

'''
def create_http_header():
    # GENERAL, REQUEST, then ENTITY
'''

# TODO: parse URL from command-line arg(s)

# TODO: Loop and redirect until we get a 200 status code (break on error)
# Initially make an HTTP call following the 1.0 specification (TODO: header formatting)
# Loop and handle each status code appropriately (5xx, 404, 401, 302, 301, 200)
# Once we hit a 200, parse and save response

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('twitter.com', 80))

# Pull URL into host param
send_request(client, '/', 'twitter.com')
response = recv_stream(client)
parsed_response_array = parse_response(response)
redirect_location = get_redirect_location(parsed_response_array)
print(parsed_response_array)
print(redirect_location)

status_code = print(get_status_code(parsed_response_array[0]))

while True:
    # Status codes can be found at /RFC1945#section-6.1.1
    # OK
    if status_code == '200': break
    # Moved Permanently
    elif status_code == '301': break
    # Moved Temporarily
    elif status_code == '302': break
    # Bad Request
    elif status_code == '400': break
    # Unauthorized
    elif status_code == '401': break
    # Not found
    elif status_code == '404': break
    # Internal Server Error
    elif status_code == '500': break
    # Not Implemented
    elif status_code == '501': break
    # Bad Gateway
    elif status_code == '502': break
    # Service Unavailable
    elif status_code == '503': break
    else: break

if requires_https(redirect_location):
    # Requires use to open and close the socket?
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sslclient = ssl.wrap_socket(client, ssl_version = ssl.PROTOCOL_TLS)
    sslclient.connect(('twitter.com', 443))
    # Reference URL into host param (varies betweeen using www.)
    # Reference redirect_location in after GET method
    send_request(sslclient, '/', 'twitter.com')
    response = recv_stream(sslclient)
    # print(response)
else:
    response = recv_stream(client)
    print(response)
    client.close()
