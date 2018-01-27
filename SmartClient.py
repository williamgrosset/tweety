import re
import sys
import lib.http_parser
import lib.socket_helper
from lib.results_logger import print_results
from lib.http2_negotiation import allows_http2

def get_url_from_args(args):
    if (len(args) != 2): print('Enter the correct amount of arguments.'); sys.exit()
    url_match = re.match('([\w\.-]*\.[\w\.-]*)', args[1], re.IGNORECASE)
    if url_match: return url_match.group(1)
    return ''

def main():
    input_url = get_url_from_args(sys.argv)
    if not input_url: print('Enter a valid url.'); return

    supports_ssl = False
    is_initial_request = True

    # Initialize and wrap socket in SSL
    client = lib.socket_helper.initialize()
    ssl_client = lib.socket_helper.ssl_wrap(client)

    # Create TCP connection
    lib.socket_helper.connect(ssl_client, input_url, 443)

    # Create and send GET request
    request = lib.socket_helper.create_request('/', input_url)
    lib.socket_helper.send(ssl_client, request)

    # Handle response segments
    response = lib.socket_helper.recv_stream(ssl_client)
    redirect_location = lib.http_parser.get_redirect_location(response)
    url = lib.http_parser.get_host_url(redirect_location)

    while True:
        status_code = lib.http_parser.get_status_code(response)

        # Success
        if status_code == '200':
            if is_initial_request: url = input_url; supports_ssl = True
            print_results(
                url,
                supports_ssl,
                lib.http_parser.get_http_version(response, allows_http2(url, supports_ssl)),
                lib.http_parser.get_cookies(response),
            )
            return
        # Moved Permanently or Found
        elif status_code == '301' or status_code == '302':
            is_initial_request = False
            redirect_location = lib.http_parser.get_redirect_location(response)
            url = lib.http_parser.get_host_url(redirect_location)
            client = lib.socket_helper.initialize()
            request = lib.socket_helper.create_request(redirect_location, url)

            if lib.http_parser.requires_https(redirect_location):
                supports_ssl = True
                ssl_client = lib.socket_helper.ssl_wrap(client)
                response = lib.socket_helper.handle_redirect(ssl_client, input_url, 443, request)
            else:
                response = lib.socket_helper.handle_redirect(client, url, 80, request)
        # Not Found
        elif status_code == '404':
            if is_initial_request: url = input_url; supports_ssl = True
            print('SmartClient was unable to find the requested resouce (404).')
            return
        # Unsupported Status Code
        else: print('SmartClient received an unsupported status code: %s.' % status_code); return

if __name__ == '__main__':
    main()
