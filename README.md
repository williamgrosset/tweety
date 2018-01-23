# tweety
:bird: A barebone HTTP client built directly using sockets.

## Notes:
+ [HTTP/1.0 RFC1945](https://tools.ietf.org/html/rfc1945)
+ [HTTP/1.1 RFC2616](https://tools.ietf.org/html/rfc2616)
+ [HTTP/2.0 RFC7540](https://tools.ietf.org/html/rfc7540)

## TODO
+ `README.md` section descriptions:
  + `.gif` demo
  + Project description
  + Assignment description
  + Command-line API
  + Console output
  + HTTP Protocol w/ TCP connection
  + SSL support
  + Sockets (Client and server — pseudo-code for both)
  + Cookies
  + URLs/URIs
  + Disclaimer
+ Clean-up `Smartclient.py`
  + Python linting module (add reference in README)
+ Error-handling for unknown hostnames
+ Test out 10 URLs
+ Output parser helper
+ Switching between protocols (test with both HTTP/1.1 and HTTP/2.0)
  + Identify highest supported HTTP version
+ Create cookie scanner helper
  + Reseach ways to grab all possible cookies (e.g Google analytic cookies?)
+ Close out all socket TCP connections? (`s.close()`)
