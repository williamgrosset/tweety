import socket
import ssl

# HTTP/2.0 Negotiation Reference: https://python-hyper.org/projects/h2/en/stable/negotiating-http2.html

def get_http2_ssl_context():
    '''
    This function creates an SSLContext object that is suitably configured for
    HTTP/2. If you're working with Python TLS directly, you'll want to do the
    exact same setup as this function does.
    '''
    # Get the basic context from the standard library.
    context = ssl.create_default_context(purpose = ssl.Purpose.SERVER_AUTH)

    # RFC 7540 Section 9.2: Implementations of HTTP/2 MUST use TLS version 1.2
    # or higher. Disable TLS 1.1 and lower.
    context.options |= (
        ssl.OP_NO_SSLv2 | ssl.OP_NO_SSLv3 | ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1
    )

    # RFC 7540 Section 9.2.1: A deployment of HTTP/2 over TLS 1.2 MUST disable
    # compression.
    context.options |= ssl.OP_NO_COMPRESSION

    # We want to negotiate using NPN and ALPN. ALPN is mandatory, but NPN may
    # be absent, so allow that. This setup allows for negotiation of HTTP/1.1.
    context.set_alpn_protocols(['h2', 'http/1.1'])

    try:
        context.set_npn_protocols(['h2', 'http/1.1'])
    except NotImplementedError:
        pass

    return context

# Wraps a HTTP/2 TLS around the TCP connection
def negotiate_tls(tcp_connection, context, url):
    # Note that SNI is mandatory for HTTP/2, so you *must* pass the
    # server_hostname argument.
    return context.wrap_socket(tcp_connection, server_hostname = url)

def supports_http2(url):
    # Step 1: Set up your TLS context.
    context = get_http2_ssl_context()

    # Step 2: Create a TCP connection.
    # Step 3: Wrap the connection in TLS and validate that we negotiated HTTP/2
    tls_connection = negotiate_tls(socket.create_connection((url, 443)), context, url)

    # Always prefer the result from ALPN to that from NPN.
    # You can only check what protocol was negotiated once the handshake is
    # complete.
    negotiated_protocol = tls_connection.selected_alpn_protocol()
    if negotiated_protocol is None:
        negotiated_protocol = tls_connection.selected_npn_protocol()

    if negotiated_protocol == "h2": return True
    return False
