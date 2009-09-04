#!/usr/bin/python
# coding=utf-8

import sys
import optparse

import myplurk
import mytweet
import myjaiku
import myfacebook
import mytumblr
import myurl
import birth

_qualifiers = { 'zh-TW': ('', '愛', '喜歡', '推', '給', '討厭', '想要', '希望',
                          '需要', '打算', '希望', '問', '已經', '曾經', '好奇', '覺得', '想', '說', '正在')
}

def plurkish_message(msg, qualifier_idx):
    if msg.startswith('http://'):
        msg = ' ' + msg
    message = _qualifiers['zh-TW'][qualifier_idx] + msg
    return message

def main():
    usage = """usage: tweeplurk.py [options] message [qualifier_idx]
Qualifiers:
""" + myplurk.get_qualifiers_string()

    parser = optparse.OptionParser(usage=usage)
    parser.add_option('-t', action="store_true", dest="testing", default=False, \
        help="testing mode")
    parser.add_option('-b', action="store_true", dest="birth", default=False, \
        help="post birth message")
    parser.add_option('-p', action="store_true", dest="plurkish", default=False, \
        help="post plurkish message")
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

    if options.plurkish == True and qualifier_idx != 0:
        message_general = plurkish_message(message_general, qualifier_idx)

    # Testing mode
    if options.testing:
        print "General:", message_general
        print "Plurk:", message_plurk, qualifier_idx
        sys.exit(1)

    clients = [
        myplurk, mytweet, myjaiku,
        myfacebook, mytumblr
    ]

    for client in clients:
        try:
            if client.__name__ == 'myplurk':
                client.send_message(message_plurk, qualifier_idx)
            else:
                client.send_message(message_general)
        except Exception:
            print "%s: Failed to post message" % client.__name__[2:]

main()
