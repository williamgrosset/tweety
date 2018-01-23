#!/usr/bin/python
import sys
import socket
import ssl
import re
from lib.cookie_parser import get_cookies
from lib.results_logger import print_results
from lib.http2_negotiation import allows_http2

def send_request(socket, location, host):
    # HTTP 1.1 (BNF grammar) (https://tools.ietf.org/html/rfc2616#section-5)
    # Request-Line *(( general-header
    #               | request-header
    #               | entity-header ) CRLF)
    #              CRLF
    # TODO: General Header: Possibly add Upgrade field for 101 (Switching Protocols) response
    REQUEST_LINE = (
        'GET ' +
        location +
        ' HTTP/1.1')
    GENERAL_HEADER = (
        'Connection: close')
    REQUEST_HEADER = (
        'Host: ' + host + '\r\n'
        # Google Chrome mock
        'User-Agent: Mozilla/5.0 (X11; CrOS i686 2268.111.0) ' +
        'AppleWebKit/536.11 (KHTML, like Gecko) ' +
        'Chrome/20.0.1132.57 Safari/536.11\r\n'
        'From: williamhgrosset@gmail.com')
    PAYLOAD = (
        REQUEST_LINE + '\r\n' +
        GENERAL_HEADER + '\r\n' +
        REQUEST_HEADER + '\r\n\r\n')

    socket.sendall(PAYLOAD.encode('utf-8'))

def recv_stream(socket):
    total_data = []
    while True:
        data = socket.recv(4096)
        if not data: break
        total_data.append(data)
    return b''.join(total_data).strip().decode('utf-8', 'ignore')

def requires_https(url):
    if url.startswith('https'): return True
    return False

def get_url_from_args(args):
    # Valid input: www.domain.com or domain.com
    if (len(args) != 2): print('Enter the correct amount of arguments.')
    url_match = re.match('([www\.]?[\w\.-]*)', args[1], re.IGNORECASE)
    if url_match: return url_match.group(1).strip()
    return ''

def get_redirect_location(response):
    location_match = re.search('Location: (http[s?]*:\/\/[\w\.-\/]+).*', response, re.IGNORECASE)
    if location_match: return location_match.group(1).strip()
    return 'Could not resolve redirect location.'

def get_host_url(location):
    location_match = re.match('http[s?]*:\/\/([\w\.-]*)\/', location, re.IGNORECASE)
    if location_match: return location_match.group(1).strip()
    return 'Could not resolve host url.'

def get_status_code(response):
    # Status codes can be found at https://tools.ietf.org/html/rfc2616#section-6.1.1
    status_code_match = re.search('HTTP\/\d\.\d (\d{3}).*', response)
    if status_code_match: return status_code_match.group(1)
    return 'No status code found.'

def get_http_version(response, supports_http2):
    if supports_http2: return 'HTTP/2.0'
    http_version_match = re.search('(HTTP\/\d\.\d) \d{3}.*', response)
    if http_version_match: return http_version_match.group(1)
    return 'No HTTP version found.'

'''
def upgrade_protocol(version):
'''

def main():
    input_url = get_url_from_args(sys.argv)
    if input_url == '': print('Please enter a valid url.'); return

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ssl_client = ssl.wrap_socket(client, ssl_version = ssl.PROTOCOL_TLS)

    ssl_client.connect((input_url, 443))
    send_request(ssl_client, '/', input_url)
    response = recv_stream(ssl_client)
    redirect_location = get_redirect_location(response)
    url = get_host_url(redirect_location)

    while True:
        status_code = get_status_code(response)

        # Switching Protocols
        if status_code == '100': break
        # OK
        elif status_code == '200':
            cookies = get_cookies(response)
            if cookies: 
                # TODO: Fix supports_https
                supports_https = requires_https(redirect_location)
                supports_http2 = allows_http2(input_url)

                print_results(
                    input_url,
                    supports_https,
                    get_http_version(response, supports_http2),
                    cookies,
                )
            else: print('No cookies found.')
            break
        # Moved Permanently or Found
        elif status_code == '301' or status_code == '302':
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            if requires_https(redirect_location):
                ssl_client = ssl.wrap_socket(client, ssl_version = ssl.PROTOCOL_TLS)
                ssl_client.connect((url, 443))
                send_request(ssl_client, redirect_location, url)
                response = recv_stream(ssl_client)
            else:
                client.connect((url, 80))
                send_request(client, redirect_location, url)
                response = recv_stream(client)

            # TODO: Verify that we won't get stuck in a 301/302
            # loop, ensure were parsing correctly
            redirect_location = get_redirect_location(response)
            url = get_host_url(redirect_location)
        # Bad Request
        elif status_code == '400':
            break
        # Not found
        elif status_code == '404': break
        # HTTP Version not supported
        elif status_code == '505': break
        else:
            print('An unsupported status code has occurred: %s' % status_code)
            break

    # Close out any remaining connections
    ssl_client.close()
    client.close()

if __name__ == '__main__':
    main()
