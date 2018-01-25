import re
import sys
import lib.http_helper
import lib.socket_helper
from lib.cookie_parser import get_cookies
from lib.results_logger import print_results
from lib.http2_negotiation import allows_http2

def get_url_from_args(args):
    # Valid input: www.domain.com or domain.com
    if (len(args) != 2): print('Enter the correct amount of arguments.')
    url_match = re.match('([www\.]?[\w\.-]*)', args[1], re.IGNORECASE)
    if url_match: return url_match.group(1).strip()
    return ''

def main():
    input_url = get_url_from_args(sys.argv)
    if input_url == '': print('Please enter a valid url.'); return

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

    status_code = lib.http_helper.get_status_code(response)
    if status_code == '200':
        supports_ssl = True
        cookies = get_cookies(response)
        supports_http2 = allows_http2(input_url, supports_ssl)
        http_version = lib.http_helper.get_http_version(response, supports_http2)

        print_results(
            input_url,
            supports_ssl,
            http_version,
            cookies,
        )
        return

    redirect_location = lib.http_helper.get_redirect_location(response)
    url = lib.http_helper.get_host_url(redirect_location)

    while True:
        status_code = lib.http_helper.get_status_code(response)

        # Switching Protocols
        if status_code == '101':
            print('Currently working on supporting 101...')
            break
        # OK
        elif status_code == '200':
            cookies = get_cookies(response)
            supports_http2 = allows_http2(input_url, supports_ssl)
            http_version = lib.http_helper.get_http_version(response, supports_http2)

            print_results(
                input_url,
                supports_ssl,
                http_version,
                cookies,
            )
            break
        # Moved Permanently or Found
        elif status_code == '301' or status_code == '302':
            # TODO: Verify that we won't get stuck in a 301/302
            # loop, ensure were parsing correctly
            redirect_location = lib.http_helper.get_redirect_location(response)
            url = lib.http_helper.get_host_url(redirect_location)

            client = lib.socket_helper.initialize()
            if lib.http_helper.requires_https(redirect_location):
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

        # Not found
        elif status_code == '404': break
        # HTTP Version not supported (maybe not necessary)
        elif status_code == '505': break
        else:
            print('An unsupported status code has occurred: %s' % status_code)
            break

    # Close out any remaining connections
    ssl_client.close()
    client.close()

if __name__ == '__main__':
    main()
