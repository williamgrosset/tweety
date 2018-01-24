import re

def print_website(url):
    print('website: ' + url)

def print_https_support(supports_https):
    if supports_https: print('1. Support of HTTPS: yes')
    else: print('1. Support of HTTPS: no')

def print_newest_http_version(http_version):
    print('2. The newest HTTP version that the web server supports: ' + http_version)

def print_cookies(cookies):
    print('3. List of cookies:')
    if cookies:
        for cookie in cookies:
            print('name: ' + cookie.name + ', key: ' + cookie.key + ', domain name: ' + cookie.domain_name)
    else:
        print('No cookies found.')

def print_results(url, supports_https, http_version, cookies):
    print_website(url)
    print_https_support(supports_https)
    print_newest_http_version(http_version)
    print_cookies(cookies)
