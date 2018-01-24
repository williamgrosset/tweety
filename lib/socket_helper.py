import sys
import ssl
import socket

def initialize():
    return socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def ssl_wrap(socket):
    return ssl.wrap_socket(socket, ssl_version = ssl.PROTOCOL_TLS)

def connect(socket, host, port):
    try:
        socket.connect((host, port))
    except Exception:
        print('Socket connection refused with host: %s, on port: %d.' % (host, port)); sys.exit()

def create_request(location, host, options = ''):
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
    return (
        REQUEST_LINE + '\r\n' +
        GENERAL_HEADER + '\r\n' +
        REQUEST_HEADER + '\r\n\r\n')

def send(socket, payload):
    socket.sendall(payload.encode('utf-8'))

def recv_stream(socket):
    total_data = []
    while True:
        data = socket.recv(4096)
        if not data: break
        total_data.append(data)
    return b''.join(total_data).strip().decode('utf-8', 'ignore')
