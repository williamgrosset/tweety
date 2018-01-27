import sys
import ssl
import socket

def initialize():
    return socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def ssl_wrap(client_socket):
    try:
        return ssl.wrap_socket(client_socket, ssl_version = ssl.PROTOCOL_TLS)
    except Exception:
        print('SmartClient was unsuccessful in wrapping socket in SSL. Try a different host.'); sys.exit()

def connect(client_socket, host, port):
    try:
        client_socket.settimeout(5)
        client_socket.connect((host, port))
        client_socket.settimeout(client_socket.gettimeout())
    except Exception:
        print('SmartClient refused connection with host: %s, on port: %d.' % (host, port)); sys.exit()

def create_request(location, host, options = ''):
    # RFC 2616 Section 5 (HTTP/1.1 BNF Grammar):
    # Request-Line *(( general-header
    #               | request-header
    #               | entity-header ) CRLF)
    #              CRLF
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

def send(client_socket, payload):
    client_socket.sendall(payload.encode('utf-8'))

def recv_stream(client_socket):
    total_data = []
    while True:
        data = client_socket.recv(4096)
        if not data: break
        total_data.append(data)
    return b''.join(total_data).strip().decode('utf-8', 'ignore')

def handle_redirect(client_socket, url, port, request):
    connect(client_socket, url, port)
    send(client_socket, request)
    return recv_stream(client_socket)
