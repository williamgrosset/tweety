import re

def print_website(url):
    print('website: ' + url)

def print_https_support(supports_https):
    if supports_https: print('1. Support of HTTPS: yes')
    else: print('1. Support of HTTPS: no')

def print_newest_http_version(http_version):
    print('2. The newest HTTP versions that the web server supports: ' + http_version)

def print_cookies(cookies):
    print('3. List of cookies:')
    name = key = domain_name = '-'

    for cookie in cookies:
        # TODO: Stricter regex
        name_match = re.match('name=(.*)', cookie)
        key_match = re.search('([\w\.-]*)=', cookie)
        domain_name_match = re.match('.*domain=([\w\.-]*)', cookie)

        if name_match: name = name_match.group(1)
        if key_match: key = key_match.group(1)
        if domain_name_match: domain_name = domain_name_match.group(1)

        print('name: ' + name + ', key: ' + key + ', domain name: ' + domain_name)

def print_results(url, supports_https, http_version, cookies):
    print_website(url)
    print_https_support(supports_https)
    print_newest_http_version(http_version)
    print_cookies(cookies)
