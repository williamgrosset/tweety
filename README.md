# wreck
:bird: A basic web client to communicate with a server via sockets.

## Notes:
+ [HTTP/1.0 RFC1945](https://tools.ietf.org/html/rfc1945)
+ [HTTP/1.1 RFC2616](https://tools.ietf.org/html/rfc2616)
+ [HTTP/2.0 RFC7540](https://tools.ietf.org/html/rfc7540)

## TODO
+ Section descriptions:
  + HTTP Protocol w/ TCP connection
  + Sockets
  + SSL support
+ Close out all socket TCP connections? (`s.close()`)
+ Create cookie scanner helper
+ Reseach ways to grab all possible cookies
+ Output parser helper
+ Switching between protocols (test with both HTTP/1.1 and HTTP/2.0)
  + Identify highest supported HTTP version
+ Clean-up `Smartclient.py`

Edge cases:
+ `400` Host-Header required
