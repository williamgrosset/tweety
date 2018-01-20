def print_website(url):
    print('website: ' + url)

def print_https_support(supports_http):
    print('1. Support of HTTPS: ' + supports_http)

def print_newest_http_version(http_version):
    print('2. The newest HTTP versions that the web server supports: ' + http_version)

def print_cookies(cookies):
    print('3. List of cookies:')

def print_results():
    print_website(url)
    print_https_support(location)
    print_newest_http_version(http_version)
    print_cookies(cookies)
