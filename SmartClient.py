#!/usr/bin/python
import sys
import socket
import ssl
import re
import cookie_helper
import results_logger

# GENERAL_HEADER = ''
# REQUEST_HEADER = 'User-Agent: ' + socket.gethostname() + '\n\n'
# ENTITY_HEADER = 'Allow: GET'

def send_request(socket, location, host):
    # TODO: Define HTTP 1.1 spec using BNF format
    # TODO: Test with HTTP/2.0 servers (see announcement)
    socket.sendall(('HEAD ' + location + ' HTTP/1.1\r\nHost: ' + host + '\r\nConnection: close' + '\r\n\r\n').encode('utf-8'))

def recv_stream(socket):
    total_data = []
    while True:
        data = socket.recv(4096)
        if not data: break
        total_data.append(data)
        # Added 'ignore' for issues with www.google.com
    return b''.join(total_data).strip().decode('utf-8', 'ignore')

def requires_https(location):
    if location.startswith('https'): return True
    return False

def get_url_from_args(args):
    if (len(args) != 2): print('Enter the correct amount of arguments.')
    # TODO: Stricter regex
    url_match = re.match('([www\.a-zA-Z0-9\.]*)', args[1])
    if url_match: return url_match.group(1).strip()
    return ''

def get_redirect_location(response):
    location_match = re.search('[L|l]ocation: (https*:\/\/[a-zA-Z0-9_\.\/]+).*', response)
    if location_match: return location_match.group(1).strip()
    return 'Could not resolve redirect location.'

def get_host_url(location):
    location_match = re.match('https*:\/\/(.*)\/', location)
    if location_match: return location_match.group(1).strip()
    return 'Could not resolve host url.'

def get_status_code(response):
    # Status codes can be found at https://tools.ietf.org/html/rfc2616#section-6.1.1
    status_code_match = re.search('HTTP\/\d\.\d (\d{3}).*', response)
    if status_code_match: return status_code_match.group(1)
    return 'No status code found.'

'''
def upgrade_protocol(version):
'''

def main():
    url = get_url_from_args(sys.argv)
    if url == '':
        print('Please enter a valid url')
        return

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ssl_client = ssl.wrap_socket(client, ssl_version = ssl.PROTOCOL_TLS)

    ssl_client.connect((url, 443))
    send_request(ssl_client, '/', url)
    response = recv_stream(ssl_client)
    print('Initial response')
    print(response)
    print('END OF BEGINNING RESPONSE')
    redirect_location = get_redirect_location(response)
    url = get_host_url(redirect_location)

    while True:
        status_code = get_status_code(response)

        # Switching Protocols
        if status_code == '100': break
        # OK
        elif status_code == '200':
            print('In 200')
            print(response)
            print('COOKIES')
            results_logger.print_cookies(cookie_helper.get_cookies(response))
            break
        # Moved Permanently or Found
        elif status_code == '301' or status_code == '302':
            print('In ' + status_code)
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            if requires_https(redirect_location):
                print('requires https')
                ssl_client = ssl.wrap_socket(client, ssl_version = ssl.PROTOCOL_TLS)
                ssl_client.connect((url, 443))
                send_request(ssl_client, redirect_location, url)
                response = recv_stream(ssl_client)
            else:
                print('does not require https')
                client.connect((url, 80))
                send_request(client, redirect_location, url)
                response = recv_stream(client)

            # TODO: Verify that we won't get stuck in a 301/302
            # loop, ensure were parsing correctly
            redirect_location = get_redirect_location(response)
            url = get_host_url(redirect_location)
        # Bad Request
        elif status_code == '400':
            print('In 400')
            break
        # Not found
        elif status_code == '404': break
        # HTTP Version not supported
        elif status_code == '505': break
        else:
            print('An unsupported status code has occurred: ' + status_code)
            break

    ssl_client.close()
    client.close()


if __name__ == '__main__':
    main()
