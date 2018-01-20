'''
def print_website(response):
    cookie_match = re.findall('Set-Cookie: (.*)', response)
    if cookie_match: print(cookie_match), print(len(cookie_match))
    else: print('None.')

def print_https_support():

def print_newest_http_version():

def print_cookies():

def print_final_results():
'''
