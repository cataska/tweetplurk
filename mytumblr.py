#!/usr/bin/python
# coding=utf-8

import sys
from tumblr import Api
import settings

def send_message(message):
    blog = settings.get('tumblr', 'blog')
    email = settings.get('tumblr', 'email')
    password = settings.get('tumblr', 'password')
    api = Api(blog, email, password)
    post = api.write_regular(None, message)
    print post['url']

def print_usage_and_exit():
    print "usage: mytumblr message"
    sys.exit(0)

def main():
    nargvs = len(sys.argv)
    if nargvs < 2:
        print_usage_and_exit()

    message = sys.argv[1]
    send_message(message)

if __name__ == '__main__':
    main()
