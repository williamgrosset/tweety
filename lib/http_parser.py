import re

class Cookie:
    name = ''
    key = ''
    domain_name = ''

    def __init__(self, name = '-', key = '-', domain_name = '-'):
        self.name = name
        self.key = key
        self.domain_name = domain_name

    def add_name(self, name):
        self.name = name

    def add_key(self, key):
        self.key = key

    def add_domain_name(self, domain_name):
        self.domain_name = domain_name

def requires_https(url):
    if url.startswith('https'): return True
    return False

def get_redirect_location(response):
    location_match = re.search('Location: (http[s?]*:\/\/[\w\.-\/]+).*', response, re.IGNORECASE)
    if location_match: return location_match.group(1)
    return 'Could not resolve redirect location.'

def get_host_url(location):
    location_match = re.match('http[s?]*:\/\/([\w\.-]*)\/', location, re.IGNORECASE)
    if location_match: return location_match.group(1)
    return 'Could not resolve host URL.'

def get_status_code(response):
    # RFC 2616 Section 6.1.1
    status_code_match = re.search('HTTP\/\d\.\d (\d{3}).*', response)
    if status_code_match: return status_code_match.group(1)
    return 'Could not resolve status code.'

def get_http_version(response, supports_http2):
    if supports_http2: return 'HTTP/2.0'
    http_version_match = re.search('(HTTP\/\d\.\d) \d{3}.*', response)
    if http_version_match: return http_version_match.group(1)
    return 'Could not resolve HTTP version.'

def get_cookies(response):
    cookie_match = re.findall('Set-Cookie: (.*)', response)
    if cookie_match:
        cookies = []
        for cookie in cookie_match:
            name_match = re.match('.*name=([\w\.-]*)', cookie)
            key_match = re.search('([\w\.-]*)=', cookie)
            domain_name_match = re.match('.*domain=([\w\.-]*)', cookie)

            cookie = Cookie()
            if name_match: cookie.add_name(name_match.group(1))
            if key_match: cookie.add_key(key_match.group(1))
            if domain_name_match: cookie.add_domain_name(domain_name_match.group(1))

            cookies.append(cookie)
        cookies.sort(key=lambda cookie: cookie.key)
        return cookies
    else: return []
