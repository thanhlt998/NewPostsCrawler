import re


def get_url_with_scheme(domain):
    return ''.join(["http://", domain])


def is_resource_url(url):
    if re.match(
            r'.*\.(css|js|bmp|gif|jpe?g|png|tiff?|mid|mp2|mp3|mp4|wav|avi|mov|mpeg|ram|m4v|pdf|rm|smil|wmv|swf|wma|zip|rar|gz|doc|docx|xls|xlsx)',
            url.lower()):
        return True
    return False


def fix_url(url):
    return re.sub("#.+", '', url)
