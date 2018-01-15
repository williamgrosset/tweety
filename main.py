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
    location_match = re.search('[L|l]ocation: (http[s*]:\/\/[a-zA-Z0-9_\.\/]+).*', response)
    if location_match: return location_match.group(1).strip()
    return 'Could not resolve redirect location.'

def get_host_domain(location):
    location_match = re.match('http[s*]:\/\/(.*)\/', location)
    if location_match: return location_match.group(1).strip()
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

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('facebook.com', 80))

# TODO: Pull URL into host param
send_request(client, '/', 'facebook.com')
response = recv_stream(client)
redirect_location = get_redirect_location(response)
host = get_host_domain(redirect_location)

while True:
    status_code = get_status_code(response)

    # OK
    if status_code == '200':
        print('In 200')
        print(response)
        client.close()
        break
    # Moved Permanently or Moved Temporarily (redirect)
    elif status_code == '301' or status_code == '302':
        if requires_https(redirect_location):
            print('In 301')
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            ssl_client = ssl.wrap_socket(client, ssl_version = ssl.PROTOCOL_TLS)
            ssl_client.connect(('facebook.com', 443))
            send_request(ssl_client, redirect_location, host)
            response = recv_stream(ssl_client)
        else:
            print('In 302')
            send_request(client, redirect_location, host)
            response = recv_stream(client)

        redirect_location = get_redirect_location(response)
        host = get_host_domain(redirect_location)
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
