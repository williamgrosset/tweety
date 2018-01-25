import re
import sys
import lib.http_parser
import lib.socket_helper
from lib.cookie_parser import get_cookies
from lib.results_logger import print_results
from lib.http2_negotiation import allows_http2

def get_url_from_args(args):
    if (len(args) != 2): print('Enter the correct amount of arguments.')
    # TODO: Stricer regex e.g require \.
    url_match = re.match('([www\.]?[\w\.-]*)', args[1], re.IGNORECASE)
    if url_match: return url_match.group(1)
    return ''

def main():
    input_url = get_url_from_args(sys.argv)
    if not input_url: print('Please enter a valid url.'); return

    # Initialize and wrap socket in SSL
    supports_ssl = False
    client = lib.socket_helper.initialize()
    ssl_client = lib.socket_helper.ssl_wrap(client)

    # Create TCP connection
    lib.socket_helper.connect(ssl_client, input_url, 443)

    # Create and send GET request
    request = lib.socket_helper.create_request('/', input_url)
    lib.socket_helper.send(ssl_client, request)

    # Handle response segments
    response = lib.socket_helper.recv_stream(ssl_client)

    status_code = lib.http_parser.get_status_code(response)
    if status_code == '200':
        supports_ssl = True
        print_results(
            input_url,
            supports_ssl,
            lib.http_parser.get_http_version(response, allows_http2(input_url, supports_ssl)),
            get_cookies(response),
        )
        return

    redirect_location = lib.http_parser.get_redirect_location(response)
    url = lib.http_parser.get_host_url(redirect_location)

    while True:
        status_code = lib.http_parser.get_status_code(response)

        # Success
        if status_code == '200':
            print_results(
                input_url,
                supports_ssl,
                lib.http_parser.get_http_version(response, allows_http2(input_url, supports_ssl)),
                get_cookies(response),
            )
            return
        # Moved Permanently or Found
        elif status_code == '301' or status_code == '302':
            # TODO: Verify that we won't get stuck in a 301/302
            # loop, ensure were parsing correctly
            client = lib.socket_helper.initialize()
            redirect_location = lib.http_parser.get_redirect_location(response)
            url = lib.http_parser.get_host_url(redirect_location)

            if lib.http_parser.requires_https(redirect_location):
                supports_ssl = True
                ssl_client = lib.socket_helper.ssl_wrap(client)

                lib.socket_helper.connect(ssl_client, input_url, 443)
                request = lib.socket_helper.create_request(redirect_location, url)
                lib.socket_helper.send(ssl_client, request)
                response = lib.socket_helper.recv_stream(ssl_client)
            else:
                lib.socket_helper.connect(client, url, 80)
                request = lib.socket_helper.create_request(redirect_location, url)
                lib.socket_helper.send(client, request)
                response = lib.socket_helper.recv_stream(client)

        # TODO: Not found
        elif status_code == '404': return
        else:
            print('An unsupported status code has occurred: %s' % status_code)
            return

    # Close out any remaining connections
    ssl_client.close()
    client.close()

if __name__ == '__main__':
    main()
