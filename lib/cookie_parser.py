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

def get_cookies(response):
    cookie_match = re.findall('Set-Cookie: (.*)', response)
    if cookie_match:
        cookies = []
        for cookie in cookie_match:
            # TODO: Stricter regex
            name_match = re.match('.*name=([\w\.-]*)', cookie)
            key_match = re.search('([\w\.-]*)=', cookie)
            domain_name_match = re.match('.*domain=([\w\.-]*)', cookie)

            # TODO: Domain name default
            cookie = Cookie()
            if name_match: cookie.add_name(name_match.group(1))
            if key_match: cookie.add_key(key_match.group(1))
            if domain_name_match: cookie.add_domain_name(domain_name_match.group(1))

            cookies.append(cookie)
        cookies.sort(key=lambda cookie: cookie.name)
        return cookies
    else: return []
