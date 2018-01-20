def print_website(url):
    cookie_match = re.findall('Set-Cookie: (.*)', response)
    if cookie_match: print(cookie_match), print(len(cookie_match))
    else: print('None.')

# def print_https_support(location):

# def print_newest_http_version(http):

# def print_cookies(cookies_collection):

'''
def print_results():
    print_website()
    print_https_support(location)
    print_cookies()
'''
