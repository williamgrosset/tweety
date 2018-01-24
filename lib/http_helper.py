import re

def requires_https(url):
    if url.startswith('https'): return True
    return False

def get_redirect_location(response):
    location_match = re.search('Location: (http[s?]*:\/\/[\w\.-\/]+).*', response, re.IGNORECASE)
    if location_match: return location_match.group(1).strip()
    return 'Could not resolve redirect location.'

def get_host_url(location):
    location_match = re.match('http[s?]*:\/\/([\w\.-]*)\/', location, re.IGNORECASE)
    if location_match: return location_match.group(1).strip()
    return 'Could not resolve host url.'

def get_status_code(response):
    # RFC2616 Section 6.1.1
    status_code_match = re.search('HTTP\/\d\.\d (\d{3}).*', response)
    if status_code_match: return status_code_match.group(1)
    return 'No status code found.'

def get_http_version(response, supports_http2):
    if supports_http2: return 'HTTP/2.0'
    http_version_match = re.search('(HTTP\/\d\.\d) \d{3}.*', response)
    if http_version_match: return http_version_match.group(1)
    return 'No HTTP version found.'
