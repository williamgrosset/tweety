#!/usr/bin/python
import sys
import socket
import ssl
import re
import http_constants  

def recv_stream(socket):
    total_data = []
    while True:
        data = socket.recv(8192)
        if not data: break
        total_data.append(data)
    return b''.join(total_data).strip().decode('utf-8')

def get_redirect_location(response):
    location_match = re.search('[L|l]ocation: (https*:\/\/[a-zA-Z0-9_\.\/]+).*', response)
    if location_match: return location_match.group(1).strip()
    return 'Could not resolve redirect location.'

def get_host_domain(location):
    location_match = re.match('https*:\/\/(.*)\/', location)
    if location_match: return location_match.group(1).strip()
    return 'Could not resolve host url.'

def requires_https(location):
    if location.startswith('https'): return True
    return False

def send_request(socket, location, host):
    # TODO: Define HTTP 1.0 spec using BNF format
    # TODO: Test with HTTP/2.0 servers
    socket.send(('GET ' + location + ' HTTP/1.0\r\nHost: ' + host + '\r\n' + http_constants.REQUEST_HEADER + '\r\n\r\n').encode('utf-8'))

def get_status_code(response):
    # Status codes can be found at https://tools.ietf.org/html/rfc1945#section-6.1.1
    status_code_match = re.search('HTTP\/\d\.\d (\d{3}).*', response)
    if status_code_match: return status_code_match.group(1)
    return 'No status code found.'

'''
def create_http_header():
    # GENERAL, REQUEST, then ENTITY
'''

def get_url_from_input(args):
    if (len(args) != 2): print('Enter the correct amount of arguments.')
    url_match = re.match('[www\.]*(.*)', args[1])
    if url_match: return url_match.group(1).strip()
    return 'Please enter a valid url.'


def main():
    url = get_url_from_input(sys.argv)
    print(url)
    # if not valid url: return

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((url, 80))

    # TODO: Pull URL into host param
    send_request(client, '/', url)
    response = recv_stream(client)
    print('Initial response')
    print(response)
    redirect_location = get_redirect_location(response)
    host_url = get_host_domain(redirect_location)

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
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            if requires_https(redirect_location):
                print('requires https')
                ssl_client = ssl.wrap_socket(client, ssl_version = ssl.PROTOCOL_TLS)
                ssl_client.connect((host_url, 443))
                send_request(ssl_client, redirect_location, host_url)
                response = recv_stream(ssl_client)
            else:
                print('does not require https')
                client.connect((host_url, 80))
                send_request(client, redirect_location, host_url)
                response = recv_stream(client)

            redirect_location = get_redirect_location(response)
            host_url = get_host_domain(redirect_location)
        # Bad Request
        elif status_code == '400':
            print(response)
            break
        # Unauthorized
        elif status_code == '401': break
        # Not found
        elif status_code == '404': break
        # Upgrade Required
        elif status_code == '426': break
        # Internal Server Error
        elif status_code == '500': break
        # Not Implemented
        elif status_code == '501': break
        # Bad Gateway
        elif status_code == '502': break
        # Service Unavailable
        elif status_code == '503': break
        else: break

if __name__ == '__main__':
    main()
