#!/usr/bin/python
# coding=utf-8

import sys
import optparse

import myplurk
import mytweet
import myjaiku
import myurl
import birth

def main():
    usage = """usage: tweeplurk.py [options] message [qualifier_idx]
Qualifiers:
""" + myplurk.get_qualifiers_string()

    parser = optparse.OptionParser(usage=usage)
    parser.add_option('-t', action="store_true", dest="testing", default=False, \
        help="testing mode")
    parser.add_option('-b', action="store_true", dest="birth", default=False, \
        help="post birth message")
    options, remainder = parser.parse_args()

    n_argv = len(sys.argv)
    if n_argv < 2:
        parser.print_help()
        sys.exit(0)

    qualifier_idx = 17 # 'says'
    if options.birth == True:
        message = str(birth.create())
        if remainder:
            qualifier_idx = int(remainder[0])
    else:
        if remainder:
            message = remainder[0]
            if len(remainder) >= 2:
                qualifier_idx = int(remainder[1])
        else:
            parser.error('There is no message to post')

    if message.startswith('http://'):
        message_general, message_plurk = myurl.httpurl_simplify(message)
    elif message.startswith('! http://'): # don't simplify the url.
        message_general, message_plurk = myurl.httpurl_simplify(message[2:], False)
    else:
        message_general = message_plurk = message

    # Testing mode
    if options.testing:
        print message_general, message_plurk, qualifier_idx
        sys.exit(1)

    try:
        myplurk.send_message(message_plurk, qualifier_idx)
    except Exception:
        print "plurk: Failed to post message"

    try:
        mytweet.send_message(message_general)
    except Exception:
        print "tweet: Failed to post message"

    try:
        myjaiku.send_message(message_general)
    except Exception:
        print "jaiku: Failed to post message"

main()
