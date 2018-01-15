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
        data = socket.recv(8192)
        if not data: break
        total_data.append(data)
    return b''.join(total_data).strip().decode('utf-8')

def get_redirect_location(response):
    location_match = re.search('[L|l]ocation: (http.*)', response)
    if location_match: return location_match.group(0)[10:]
    return 'Could not resolve redirect location.'

def get_host_domain(location):
    location_match = re.match('http[s*]:\/\/(.*)\/', location)
    if location_match: return location_match.group(1)
    return 'Could not resolve host url.'

def requires_https(location):
    if location.startswith('https'): return True
    else: return False

def send_request(socket, location, host):
    # TODO: Define HTTP 1.0 spec using BNF format
    # TODO: Test with HTTP/2.0 servers
    socket.send(('GET ' + location + ' HTTP/1.0\r\nHost: ' + host + '\r\n' + REQUEST_HEADER + '\r\n\r\n').encode('utf-8'))

def get_status_code(response):
    # Status codes can be found at https://tools.ietf.org/html/rfc1945#section-6.1.1
    status_code_match = re.search('HTTP\/\d\.\d (\d{3}).*', response)
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

# TODO: Pull URL into host param
send_request(client, '/', 'twitter.com')
response = recv_stream(client)

while True:
    status_code = get_status_code(response)
    # TODO: Don't update these variables here
    redirect_location = get_redirect_location(response)
    print(redirect_location)
    host = get_host_domain(redirect_location)

    # OK
    if status_code == '200':
        print('In 200')
        print(response)
        client.close()
        break
    # Moved Permanently or Moved Temporarily (redirect)
    elif status_code == '301' or status_code == '302':
        if requires_https(redirect_location):
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            ssl_client = ssl.wrap_socket(client, ssl_version = ssl.PROTOCOL_TLS)
            ssl_client.connect(('twitter.com', 443))
            send_request(ssl_client, '/', host)
            response = recv_stream(ssl_client)
        else:
            send_request(client, '/', host)
            response = recv_stream(client)
    # Bad Request
    elif status_code == '400':
        print(response)
        break
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
