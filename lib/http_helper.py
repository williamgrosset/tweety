import re
from lib.cookie_parser import get_cookies
from lib.results_logger import print_results
from lib.http2_negotiation import allows_http2

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

def requires_https(url):
    if url.startswith('https'): return True
    return False

def get_redirect_location(response):
    location_match = re.search('Location: (http[s?]*:\/\/[\w\.-\/]+).*', response, re.IGNORECASE)
    if location_match: return location_match.group(1).strip()
    return 'Could not resolve redirect location.'

def get_host_url(location):
    location_match = re.match('http[s?]*:\/\/([\w\.-]*)\/', location, re.IGNORECASE)
    if location_match: return location_match.group(1).strip()
    return 'Could not resolve host url.'

def get_status_code(response):
    # RFC2616 Section 6.1.1
    status_code_match = re.search('HTTP\/\d\.\d (\d{3}).*', response)
    if status_code_match: return status_code_match.group(1)
    return 'No status code found.'

def get_http_version(response, supports_http2):
    if supports_http2: return 'HTTP/2.0'
    http_version_match = re.search('(HTTP\/\d\.\d) \d{3}.*', response)
    if http_version_match: return http_version_match.group(1)
    return 'No HTTP version found.'

def handle_successful_request(response, input_url, supports_ssl):
    cookies = get_cookies(response)
    supports_http2 = allows_http2(input_url, supports_ssl)

    print_results(
        input_url,
        supports_ssl,
        get_http_version(response, supports_http2),
        cookies,
    )
