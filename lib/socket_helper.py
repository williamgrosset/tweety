import sys
from lib.cookie_parser import get_cookies
from lib.results_logger import print_results
from lib.http2_negotiation import allows_http2
from lib.http_helper import get_http_version 

def connect(socket, host, port):
    try:
        socket.connect((host, port))
    except Exception:
        print('Socket connection refused with host: %s, on port: %d.' % (host, port)); sys.exit()

def send_request(socket, location, host, options = ''):
    # RFC2616 Section 5 (HTTP/1.1 BNF Grammar):
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
        # Google Chrome User-Agent mock
        'User-Agent: Mozilla/5.0 (X11; CrOS i686 2268.111.0) ' +
        'AppleWebKit/536.11 (KHTML, like Gecko) ' +
        'Chrome/20.0.1132.57 Safari/536.11\r\n' +
        options +
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

def handle_successful_request(response, input_url, supports_ssl):
    cookies = get_cookies(response)
    supports_http2 = allows_http2(input_url, supports_ssl)

    print_results(
        input_url,
        supports_ssl,
        get_http_version(response, supports_http2),
        cookies,
    )
