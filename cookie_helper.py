import re

def get_cookies(response):
    cookie_match = re.search('Set-Cookie: (.*)', response)
    if cookie_match: print(cookie_match.group())
    else: print('None.')
