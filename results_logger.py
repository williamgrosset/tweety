import re

def print_website(url):
    print('website: ' + url)

def print_https_support(supports_http):
    print('1. Support of HTTPS: ' + supports_http)

def print_newest_http_version(http_version):
    print('2. The newest HTTP versions that the web server supports: ' + http_version)

def print_cookies(cookies):
    print('3. List of cookies:')
    print(cookies)
    for cookie in cookies:
        name = '-'
        key = ''
        domain_name = ''

        name_match = re.search('name=(.*)[\r]', cookie)
        key_match = re.search('(.*);', cookie)
        domain_name_match = re.search('domain=(.*)[\r]', cookie)

        print(name + ', ' + key + ', ' + domain_name)

def print_results():
    print_website(url)
    print_https_support(location)
    print_newest_http_version(http_version)
    print_cookies(cookies)
