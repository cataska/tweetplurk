#!/usr/bin/python

import sys
import urllib

MAX_LEN = len('http://tinyurl.com/123456')

def tiny_url(url):
    if MAX_LEN >= len(url):
        return url

    apiurl = "http://tinyurl.com/api-create.php?url="
    tinyurl = urllib.urlopen(apiurl + url).read()
    return tinyurl

if __name__ == '__main__':
    print tiny_url(sys.argv[1])

