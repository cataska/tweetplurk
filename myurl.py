#!/usr/bin/python

import re
import tinyurl

def httpurl_simplify(url, simplify=True):
    http_url = re.match('(^http:\/\/[^ ]*)', url).group(1)
    if simplify == True:
        http_url = tinyurl.tiny_url(http_url) 

    desc_match = re.match('^http:\/\/[^ ]* (.*)', url)
    if desc_match == None:
        str_general = http_url
        str_plurk = str_general
    else:
        description = desc_match.group(1)
        str_general = '%s # %s' % (http_url, description)
        str_plurk = '%s (%s)' % (http_url, description)

    return (str_general, str_plurk)

if __name__ == '__main__':
    import sys
    general, plurk = httpurl_simplify(sys.argv[1])
    print general
    print plurk
