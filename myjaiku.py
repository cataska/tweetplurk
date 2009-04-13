#!/usr/bin/python
# coding=utf-8

import sys
from ConfigParser import ConfigParser
import jaiku

rc_name = 'tweetplurk.rc'

def send_message(message):
	config = ConfigParser()
	config.read(rc_name)
	username = config.get('jaiku', 'username')
	apikey = config.get('jaiku', 'apikey')

	japi = jaiku.Api(username=username, api_key=apikey)
	print japi.PostPresence(message)

def print_usage_and_exit():
	print "usage: myjaiku message"
	sys.exit(0)

def main():
	nargvs = len(sys.argv)
	if nargvs < 2:
		print_usage_and_exit()

	message = sys.argv[1]
	send_message(message)

if __name__ == '__main__':
	main()
