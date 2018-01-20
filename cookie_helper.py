import re

def get_cookies(response):
    cookie_match = re.findall('Set-Cookie: (.*)', response)
    if cookie_match: return cookie_match
    else: print('None.')

# TODO: Helper functions to retrieve all possible cookies
