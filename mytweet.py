#!/usr/bin/python
# coding=utf-8 

import sys
from ConfigParser import ConfigParser
import twitter

rc_name = 'tweetplurk.rc'

def send_message(message):
	config = ConfigParser()
	config.read(rc_name)
	username = config.get('tweet', 'username')
	password = config.get('tweet', 'password')

	api = twitter.Api(username=username, password=password, input_encoding='utf-8')
	status = api.PostUpdate(message)
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
