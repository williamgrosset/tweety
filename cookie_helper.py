import re

def get_cookies(response):
    cookie_match = re.findall('Set-Cookie: (.*)', response)
    if cookie_match: print(cookie_match), print(len(cookie_match))
    else: print('None.')

# TODO: Helper functions to retrieve all possible cookies
