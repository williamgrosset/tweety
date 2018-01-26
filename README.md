# tweety
:bird: A barebone HTTP client built directly with sockets.

gif

## Overview
+ Project description
+ Assignment description
+ RFC guidelines

### Usage 
```bash
$ python3 SmartClient.py www.google.com

# Example Output
website: www.google.com
1. Support of HTTPS: yes
2. The newest HTTP version that the web server supports: HTTP/2.0
3. List of cookies:
name: -, key: 1P_JAR, domain name: .google.ca
name: -, key: NID, domain name: .google.ca
```

### Helper Libaries
```bash
$ cd <PROJECT-PATH>/lib/
http2_negotiation.py  results_logger.py
http_parser.py        socket_helper.py
```

### HTTP Protocol
...

### HTTP/2.0 Support
+ Include console output

### SSL Support
...

### Sockets and TCP Connection
+ Sockets (Client and server — pseudo-code for both)

### Cookies
...

## Disclaimer
There are status codes that are not supported to reduce the scope of assignment requirements. This is my first time building a project with Python and the code has not been peer-reviewed.

## TODO
+ Clean-up `Smartclient.py`
+ Error-handling for unknown hostnames
+ Close out all socket TCP connections? (`s.close()`)
+ Test on Linux (ssh)
+ `README.md` section descriptions

### References
+ [HTTP/1.0 RFC1945](https://tools.ietf.org/html/rfc1945)
+ [HTTP/1.1 RFC2616](https://tools.ietf.org/html/rfc2616)
+ [HTTP/2.0 RFC7540](https://tools.ietf.org/html/rfc7540)
+ [HTTP/2.0 Negotiation](https://python-hyper.org/projects/h2/en/stable/negotiating-http2.html)
