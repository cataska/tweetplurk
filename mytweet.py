#!/usr/bin/python
# coding=utf-8 

import sys
import twitter
import settings
from urllib2 import HTTPError

def send_message(message):
    username = settings.get('tweet', 'username')
    password = settings.get('tweet', 'password')

    api = twitter.Api(username=username, password=password, input_encoding='utf-8')
    count = 5
    while count > 0:
        try:
            status = api.PostUpdate(message)
            break
        except HTTPError, e:
            if 408 == e.code:
                print "mytweet: retrying..."
                count -= 1
                continue

    print status.text

def print_usage_and_exit():
    print "usage: mytweet message"
    sys.exit(0)

def main():
    nargvs = len(sys.argv)
    if nargvs < 2:
        print_usage_and_exit()

    message = sys.argv[1]
    send_message(message)

if __name__ == '__main__':
    main()
