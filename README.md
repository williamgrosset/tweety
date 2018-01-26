# tweety
:bird: A barebone HTTP client built directly with sockets.

gif

## Overview
+ Project description
+ Assignment description
+ RFC guidelines

### Usage 
```python
$ python3 SmartClient.py www.google.com
```

### Helper Libaries
...

### HTTP Protocol
...

### HTTP/2 Support
+ Include console output

### SSL Support
...

### Sockets and TCP Connection
+ Sockets (Client and server — pseudo-code for both)

### Cookies
...

## Disclaimer
This is my second time writing Python. There status codes that are **not** supported to reduce the scope of assignment requirements.

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
