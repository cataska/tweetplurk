#!/usr/bin/python
# coding=utf-8

import sys
import facebook
import settings

def send_message(message):
    apikey = settings.get('facebook', 'apikey')
    secretkey = settings.get('facebook', 'sessionkey')
    fb = facebook.Facebook(apikey, secretkey)
    fb.session_key = settings.get('facebook', 'sessionkey')
    fb.secret = settings.get('facebook', 'secret')
    fb.status.set([message])

def print_usage_and_exit():
    print "usage: myfacebook message"
    sys.exit(0)

def main():
    nargvs = len(sys.argv)
    if nargvs < 2:
        print_usage_and_exit()

    message = sys.argv[1]
    send_message(message)

if __name__ == '__main__':
    main()
