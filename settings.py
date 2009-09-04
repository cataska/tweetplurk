
from ConfigParser import ConfigParser

config = ConfigParser()
config.read('tweetplurk.rc')

def get(section, option):
    return config.get(section, option)
