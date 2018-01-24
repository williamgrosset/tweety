import sys
import socket
import ssl
import re
import lib.http_helper 

def get_url_from_args(args):
    # Valid input: www.domain.com or domain.com
    if (len(args) != 2): print('Enter the correct amount of arguments.')
    url_match = re.match('([www\.]?[\w\.-]*)', args[1], re.IGNORECASE)
    if url_match: return url_match.group(1).strip()
    return ''

def main():
    input_url = get_url_from_args(sys.argv)
    if input_url == '': print('Please enter a valid url.'); return

    # Wrap socket in SSL initially
    supports_ssl = False
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ssl_client = ssl.wrap_socket(client, ssl_version = ssl.PROTOCOL_TLS)

    # Create TCP connection and send request
    ssl_client.connect((input_url, 443))
    lib.http_helper.send_request(ssl_client, '/', input_url)

    # Handle response segments
    response = lib.http_helper.recv_stream(ssl_client)

    status_code = lib.http_helper.get_status_code(response)
    if status_code == '200':
        supports_ssl = True
        lib.http_helper.handle_successful_request(response, input_url, supports_ssl)
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
            lib.http_helper.handle_successful_request(response, input_url, supports_ssl)
            break
        # Moved Permanently or Found
        elif status_code == '301' or status_code == '302':
            # TODO: Verify that we won't get stuck in a 301/302
            # loop, ensure were parsing correctly
            redirect_location = lib.http_helper.get_redirect_location(response)
            url = lib.http_helper.get_host_url(redirect_location)

            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            if lib.http_helper.requires_https(redirect_location):
                supports_ssl = True
                ssl_client = ssl.wrap_socket(client, ssl_version = ssl.PROTOCOL_TLS)
                ssl_client.connect((url, 443))
                lib.http_helper.send_request(ssl_client, redirect_location, url)
                response = lib.http_helper.recv_stream(ssl_client)
            else:
                client.connect((url, 80))
                lib.http_helper.send_request(client, redirect_location, url)
                response = lib.http_helper.recv_stream(client)

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
