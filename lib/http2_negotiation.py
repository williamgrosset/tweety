import sys
import ssl
import lib.http_parser
import lib.socket_helper

# HTTP/2.0 Negotiation Reference: https://python-hyper.org/projects/h2/en/stable/negotiating-http2.html

def get_http2_ssl_context():
    context = ssl.create_default_context(purpose = ssl.Purpose.SERVER_AUTH)

    # RFC7540 Section 9.2: HTTP/2 requires TLS version 1.2 or higher. Disable TLS 1.1 and lower.
    context.options |= (
        ssl.OP_NO_SSLv2 |
        ssl.OP_NO_SSLv3 |
        ssl.OP_NO_TLSv1 |
        ssl.OP_NO_TLSv1_1
    )

    # RFC7540 Section 9.2.1: HTTP/2 over TLS 1.2 MUST disable compression.
    context.options |= ssl.OP_NO_COMPRESSION

    try:
        context.set_alpn_protocols(['h2', 'http/1.1'])
        context.set_npn_protocols(['h2', 'http/1.1'])
    except Exception:
        pass

    return context

# Cannot use lib/socket_helper (necessary for server_hostname parameter)
def negotiate_tls(tcp_connection, context, url):
    try:
        return context.wrap_socket(tcp_connection, server_hostname = url)
    except Exception:
        # Bypass SSL wrap error to continue printing results
        pass

def allows_http2(url, supports_ssl):
    client = lib.socket_helper.initialize()

    if supports_ssl:
        context = get_http2_ssl_context()

        lib.socket_helper.connect(client, url, 443)
        tls_connection = negotiate_tls(client, context, url)

        if tls_connection: negotiated_protocol = tls_connection.selected_alpn_protocol()
        else: return False

        if negotiated_protocol is None: negotiated_protocol = tls_connection.selected_npn_protocol()
        if negotiated_protocol == 'h2': return True
    else:
        lib.socket_helper.connect(client, url, 80)
        request = lib.socket_helper.create_request('/', url, 'Upgrade: h2c\r\n')
        lib.socket_helper.send(client, request)

        response = lib.socket_helper.recv_stream(client)

        if lib.http_parser.get_status_code(response) == '101': return True
    return False
