#!/usr/bin/python
# coding=utf-8

import sys
from ConfigParser import ConfigParser
import facebook

rc_name = "tweetplurk.rc"

def send_message(message):
    config = ConfigParser()
    config.read(rc_name)
    apikey = config.get('facebook', 'apikey')
    secretkey = config.get('facebook', 'sessionkey')
    fb = facebook.Facebook(apikey, secretkey)
    fb.session_key = config.get('facebook', 'sessionkey')
    fb.secret = config.get('facebook', 'secret')
    fb.status.set([message])

def main():
	nargvs = len(sys.argv)
	if nargvs < 2:
		print_usage_and_exit()

	message = sys.argv[1]
	send_message(message)

if __name__ == '__main__':
	main()
