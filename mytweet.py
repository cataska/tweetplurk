#!/usr/bin/python
# coding=utf-8 

import sys
import tweepy
import settings
import ConfigParser
from urllib2 import HTTPError

def send_message(message):
    username = settings.get('tweet', 'username')
    password = settings.get('tweet', 'password')
    appkey = settings.get('tweet', 'appkey')
    appsecret = settings.get('tweet', 'appsecret')
    try:
        userkey = settings.get('tweet', 'userkey')
        usersecret = settings.get('tweet', 'usersecret')
    except ConfigParser.NoOptionError:
        userkey = ''
        usersecret = ''

    auth = tweepy.OAuthHandler(appkey, appsecret)
    if userkey == '':
        print 'Authorization URL: ' + auth.get_authorization_url()
        verifier = raw_input('Verifier:')
        auth.get_access_token(verifier)
        print "userkey = " + auth.access_token.key
        print "usersecret = " + auth.access_token.secret
    else:
        auth.set_access_token(userkey, usersecret)
    api = tweepy.API(auth)
    count = 5
    while count > 0:
        try:
            status = api.update_status(message)
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
