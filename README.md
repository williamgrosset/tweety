# tweety
:bird: A barebone HTTP client built directly with sockets.

![alt text](https://github.com/williamgrosset/tweety/blob/master/example.gif "SmartClient example")

## TODO
+ Clean-up `SmartClient.py`
  + handle 404, 505 appropriately?
+ Error-handling for unknown hostnames
+ Close out all socket TCP connections? (`s.close()`)
+ Test on Linux (ssh)
+ Test all URLs
+ Section descriptions: HTTP protocol, h2, ssl, sockets (tcp connection with client & server), cookies

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
$ python3 SmartClient.py www.uvic.ca

website: www.uvic.ca
1. Support of HTTPS: yes
2. The newest HTTP version that the web server supports: HTTP/1.1
3. List of cookies:
name: -, key: SESSID_UV_128004, domain name: www.uvic.ca
name: -, key: uvic_bar, domain name: .uvic.ca
name: -, key: www_def, domain name: -
name: -, key: TS01a564a5, domain name: -
name: -, key: TS01c8da3c, domain name: www.uvic.ca
name: -, key: TS014bf86f, domain name: .uvic.ca
```

### Project Layout
`SmartClient` is the main entry point and uses the custom helper files outlined below. Only the following Python libaries are used: `re`, `sys`, `socket`, `ssl`.

```bash
$ cd <PROJECT-PATH>/lib/
http2_negotiation.py  results_logger.py
http_parser.py        socket_helper.py
```

### References
+ [HTTP/1.0 RFC1945](https://tools.ietf.org/html/rfc1945)
+ [HTTP/1.1 RFC2616](https://tools.ietf.org/html/rfc2616)
+ [HTTP/2.0 RFC7540](https://tools.ietf.org/html/rfc7540)
+ [HTTP/2.0 Negotiation](https://python-hyper.org/projects/h2/en/stable/negotiating-http2.html)
