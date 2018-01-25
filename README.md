# tweety
:bird: A barebone HTTP client built directly with sockets.

gif

## Overview
+ Project description
+ Assignment description
+ RFC Guidelines

### Command-line interface
`$ python3 SmartClient.py www.google.com`

### Helper libaries
...

### HTTP protocol
...

### HTTP/2 support
+ Include console output

### SSL support
...

### Sockets and TCP connection
+ Sockets (Client and server — pseudo-code for both)

### Cookies
...

## Disclaimer
...

## TODO
+ `README.md` section descriptions:
+ Clean-up `Smartclient.py`
  + Python linting module (add reference in README)
+ Error-handling for unknown hostnames
+ Switching between protocols (test with both HTTP/1.1 and HTTP/2.0)
  + Identify highest supported HTTP version
+ Close out all socket TCP connections? (`s.close()`)
+ Cookie domain name defaulting
+ Test on Linux (ssh)

### References
+ [HTTP/1.0 RFC1945](https://tools.ietf.org/html/rfc1945)
+ [HTTP/1.1 RFC2616](https://tools.ietf.org/html/rfc2616)
+ [HTTP/2.0 RFC7540](https://tools.ietf.org/html/rfc7540)
+ [HTTP/2.0 Negotiation](https://python-hyper.org/projects/h2/en/stable/negotiating-http2.html)
