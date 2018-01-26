# tweety
:bird: A barebone HTTP client built directly with sockets.

![alt text](https://github.com/williamgrosset/tweety/blob/master/example.gif "SmartClient example")

## TODO
+ Clean-up `SmartClient.py`
  + handle 404, 505 appropriately?
+ Error-handling for unknown hostnames
+ Close out all socket TCP connections? (`s.close()`)
+ Test on Linux (ssh)

## Overview
This project was designed for an assignment during the [Computer Communications and Networks](https://github.com/williamgrosset/tweety/blob/master/csc361_p1.pdf) class. The purpose of this client is to support a `GET` request to a web server over the HTTP protocol. `SmartClient` will echo web server's support for HTTPs, highest HTTP version, and the available cookies. See references below for RFC papers (1945, 2616, 7450) outlining the HTTP/(1.0, 1.1, 2.0) protocol.

### Usage 
```bash
# Prerequisite: Python 3.6.4
# Example 1
$ python3 SmartClient.py www.google.com

website: www.google.com
1. Support of HTTPS: yes
2. The newest HTTP version that the web server supports: HTTP/2.0
3. List of cookies:
name: -, key: 1P_JAR, domain name: .google.ca
name: -, key: NID, domain name: .google.ca

# Example 2
$ python3 SmartClient.py www.facebook.ca

website: www.facebook.com
1. Support of HTTPS: yes
2. The newest HTTP version that the web server supports: HTTP/2.0
3. List of cookies:
name: -, key: fr, domain name: .facebook.com
name: -, key: sb, domain name: .facebook.com
```

### Project Layout
`SmartClient` is the main entry point and uses the custom helper files outlined below. Only the following Python libaries are used: `re`, `sys`, `socket`, `ssl`.

```bash
$ cd <PROJECT-PATH>/lib/
http2_negotiation.py  results_logger.py
http_parser.py        socket_helper.py
```

### HTTP Protocol
...

### HTTP/2.0 Support
...

### SSL Support
...

### Sockets and TCP Connection
Sockets provide an API to the network layer to create a TCP connection for our HTTP request.

#### Client
+ pseudo-code

#### Server
+ pseudo-code

### Cookies
...

### Disclaimer
There are status codes that are not supported to reduce the scope of assignment requirements. This is my first time building a project with Python and the code has not been peer-reviewed.

### References
+ [HTTP/1.0 RFC1945](https://tools.ietf.org/html/rfc1945)
+ [HTTP/1.1 RFC2616](https://tools.ietf.org/html/rfc2616)
+ [HTTP/2.0 RFC7540](https://tools.ietf.org/html/rfc7540)
+ [HTTP/2.0 Negotiation](https://python-hyper.org/projects/h2/en/stable/negotiating-http2.html)
