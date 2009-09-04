#!/usr/bin/python
# coding=utf-8

import sys
import plurkapi
import settings

def print_qualifiers():
    i = 0
    for qualifier in plurkapi.PlurkAPI._qualifiers['en']:
        print "%d %s" % (i, qualifier)
        i += 1

def get_qualifiers_string():
    str = ""
    i = 0
    for qualifier in plurkapi.PlurkAPI._qualifiers['en']:
        str += "%d %s\n" % (i, qualifier)
        i += 1

    return str

def send_message(message, qualifier_idx=0):
    pnickname = settings.get('plurk', 'username')
    ppassword = settings.get('plurk', 'password')

    qualifier = 'says'
    if qualifier_idx < len(plurkapi.PlurkAPI._qualifiers['en']):
        qualifier = plurkapi.PlurkAPI._qualifiers['en'][qualifier_idx]

    papi = plurkapi.PlurkAPI()
    if papi.login(pnickname, ppassword) == False:
        print "login fail"
    else:
        print papi.addPlurk(qualifier=qualifier, content=message, lang="tr_ch")

def print_usage_and_exit():
    print "usage: myplurk message [qualifier_idx]"
    print_qualifiers()
    sys.exit(0)

def main():
    nargvs = len(sys.argv)
    if nargvs < 2:
        print_usage_and_exit()

    message = sys.argv[1]
    qualifier_idx = 17 # 'says'
    if nargvs >= 3:
        qualifier_idx = int(sys.argv[2])

    send_message(message, qualifier_idx)

if __name__ == '__main__':
    main()
