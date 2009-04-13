#!/usr/bin/env python
#
# Copyright 2007 Google Inc. All Rights Reserved.

""" Library that provides access to the Jaiku API. Heavily, HEAVILY based on python-twitter by DeWitt Clinton ( dewitt@google.com ), 
    which was released under the Apache license.  And by "heavily" I mean that most if is literally copy/pasted and modified to work with 
    the slightly-different-but-still-similar JSON api from Jaiku. """

__author__ = 'michael@geekfire.com'
__version__ = '0.1'

import os
import time
import tempfile
import simplejson
import md5
import urllib
import urllib2
import urlparse
import jaiku
import sys

ICON_DICT = {
  'car': '301',
  'alarm clock': '302',
  'loudspeaker': '303',
  'tram': '304',
  'casette': '305',
  'underwear': '306',
  'rollerblade': '307',
  'uzi': '308',
  'scoop': '309',
  'bomb': '310',
  'bra': '311',
  'videotape': '312',
  'cigarettes': '313',
  'vinyl': '314',
  'champaign': '315',
  'airport': '316',
  'bus': '317',
  'grumpy': '318',
  'coffee': '319',
  'camera': '320',
  'basketball': '321',
  'beer': '322',
  'binoculars': '323',
  'boiler': '324',
  'walk': '325',
  'wallclock': '326',
  'trashcan': '327',
  'tv': '328',
  'computer': '329',
  'videocamera': '330',
  'game': '331',
  'cone': '332',
  'driller': '333',
  'popcorn': '334',
  'play': '335',
  'disc': '336',
  'event': '337',
  'exclamationmark': '338',
  'football': '339',
  'fork': '341',
  'gameboy': '342',
  'grenade': '343',
  'hand': '344',
  'hanger': '345',
  'ear muffs': '346',
  'love': '347',
  'balloons': '348',
  'clock': '349',
  'barrier': '350',
  'megaphone': '352',
  'microwave': '353',
  'book': '354',
  'middle finger': '355',
  'notes': '356',
  'question': '357',
  'rollator': '358',
  'shuttlecock': '359',
  'salt': '360',
  'scull': '361',
  'sk8': '362',
  'leep': '363',
  'snorkeling': '364',
  'snowflake': '365',
  'soda': '366',
  'song': '367',
  'spray': '368',
  'sticks': '369',
  'storm': '370',
  'straitjacket': '371',
  'metro': '372',
  'luggage': '373',
  'sun': '374',
  'taxi': '375',
  'technics': '376',
  'toaster': '377',
  'train': '378',
  'wheelchair': '379',
  'zippo': '380',
  'ice cream': '381',
  'movie': '382',
  'makeup': '383',
  'bandaid': '384',
  'wine': '385',
  'clean': '386',
  'blading': '387',
  'bike': '388',
  'pils': '389',
  'picnic': '390',
  'lifejacket': '391',
  'home': '392',
  'happy': '393',
  'toiletpaper': '394',
  'theatre': '395',
  'shop': '396',
  'search': '397',
  'cloudy': '398',
  'hurry': '399',
  'morning': '400',
  'itsaboy': '402',
}

class JaikuException(Exception):
  """ Base class for Jaiku-related exceptions."""

class Presence(object):
  '''A class representing the Presence structure used by the Jaiku API.

  The Presence structure exposes the following properties:

    Presence.created_at
    Presence.created_at_in_seconds # read only
    Presence.id
    Presence.title
    Presence.relative_created_at # read only
    Presence.user
  '''
  def __init__(self,
               created_at=None,
               id=None,
               comment_id=None,
               title=None,
               content=None,
               pretty_content=None,
               user=None,
               created_at_relative=None,
               comments=None,
               icon=None,
               url=None,
               location=None):
    '''An object to hold a Jaiku Presence message.

    This class is normally instantiated by the Jaiku.Api class and
    returned in a sequence.

    Note: Dates are posted in the form "2008-01-15T23:38:56 GMT"

    Args:
      created_at: The time this Presence message was posted
      id: The unique id of this Presence message
      title: The text of this Presence message
      relative_created_at:
        A human readable string representing the posting time
      user:
        A jaiku.User instance representing the person posting the message
      now:
        The current time, if the client choses to set it.  Defaults to the
        wall clock time.
    '''
    self.created_at = created_at
    self.id = id
    if comment_id:
      self.id = comment_id
    self.title = title
    self.content = content
    self.pretty_content = pretty_content
    self.user = user
    self.created_at_relative = created_at_relative
    self.comments = comments
    self.icon = icon
    self.location = location
    self.url = url

  def GetCreatedAt(self):
    '''Get the time this Presence message was posted.

    Returns:
      The time this Presence message was posted
    '''
    return self._created_at

  def SetCreatedAt(self, created_at):
    '''Set the time this Presence message was posted.

    Args:
      created_at: The time this Presence message was created
    '''
    self._created_at = created_at

  created_at = property(GetCreatedAt, SetCreatedAt,
                        doc='The time this Presence message was posted.')

  def GetCreatedAtInSeconds(self):
    '''Get the time this Presence message was posted, in seconds since the epoch.

    Returns:
      The time this Presence message was posted, in seconds since the epoch.
    '''
    return time.mktime(time.strptime(self.created_at, '%Y-%m-%dT%H:%M:%S %Z'))

  created_at_in_seconds = property(GetCreatedAtInSeconds,
                                   doc="The time this Presence message was "
                                       "posted, in seconds since the epoch")

  def GetId(self):
    '''Get the unique id of this Presence message.

    Returns:
      The unique id of this Presence message
    '''
    return self._id

  def SetId(self, id):
    '''Set the unique id of this Presence message.

    Args:
      id: The unique id of this Presence message
    '''
    self._id = id

  id = property(GetId, SetId,
                doc='The unique id of this Presence message.')

  def GetTitle(self):
    '''Get the title of this Presence message.

    Returns:
      The title of this Presence message.
    '''
    return self._title

  def SetTitle(self, title):
    '''Set the title of this Presence message.

    Args:
      text: The title of this Presence message
    '''
    self._title = title

  title = property(GetTitle, SetTitle,
                  doc='The text of this Presence')

  def GetContent(self):
    '''Get the content of this Presence message.

    Returns:
      The content of this Presence message.
    '''    
    return self._content
    
  def SetContent(self, content):
    '''Set the content of this Presence message.

    Args:
      content: The content of this Presence message
    '''
    self._content = content
  
  content = property(GetContent, SetContent,
                    doc='The content, if any, of this Presence.')
  
  def GetPrettyContent(self):
    '''Get the pretty content of this Presence message.

    Returns:
      The pretty content of this Presence message.
    '''    
    return self._pretty_content
    
  def SetPrettyContent(self, pretty_content):
    '''Set the pretty content of this Presence message.

    Args:
      pretty_content: The pretty content of this Presence message
    '''
    self._pretty_content = pretty_content
  
  pretty_content = property(GetPrettyContent, SetPrettyContent,
                    doc='The pretty content, if any, of this Presence.')

  def GetUser(self):
    '''Get a jaiku.User reprenting the entity posting this Presence message.

    Returns:
      A jaiku.User reprenting the entity posting this Presence message
    '''
    return self._user

  def SetUser(self, user):
    '''Set a jaiku.User reprenting the entity posting this Presence message.

    Args:
      user: A jaiku.User reprenting the entity posting this Presence message
    '''
    self._user = user

  user = property(GetUser, SetUser,
                  doc='A jaiku.User reprenting the entity posting this '
                      'Presence message')
                      
  def GetRelativeCreatedAt(self):
    '''Get the time this Presence message was posted.

    Returns:
      The time this Presence message was posted
    '''
    return self._created_at_relative

  def SetRelativeCreatedAt(self, created_at_relative):
    '''Set the time this Presence message was posted.

    Args:
      created_at: The time this Presence message was created
    '''
    self._created_at_relative = created_at_relative
    
  created_at_relative = property(GetRelativeCreatedAt, SetRelativeCreatedAt,
                  doc='Get a human readable stream of the relative time this Presence was posted.')

  def GetIcon(self):
    '''Get the url for the icon of this Presence.

    Returns:
      The URL icon  this Presence message was posted
    '''
    return self._icon

  def SetIcon(self, icon):
    '''Set the url for the icon of this Presence.

    Args:
      icon: The url for the icon of this Presence
    '''
    self._icon = icon
    
  icon = property(GetIcon, SetIcon,
                  doc='Get the URL of the icon used for this Presence.')

  def GetComments(self):
    '''Get the number of comments this Presence has.

    Returns:
      The number of comments this Presence has
    '''
    return self._comments

  def SetComments(self, comments):
    '''Set the number of comments this Presence has.
    
    Args:
      comments: The number of comments this Presence has
    '''
    self._comments = comments
    
  comments = property(GetComments, SetComments,
                  doc='Get the number of comments this Presence has.')

  def GetUrl(self):
    '''Get the url of this Presence message.

    Returns:
      The url of this Presence message.
    '''    
    return self._url
    
  def SetUrl(self, url):
    '''Set the url of this Presence message.

    Args:
      url: The url of this Presence message
    '''
    self._url = url
  
  url = property(GetUrl, SetUrl,
                    doc='The url of this presence.')
                  
  def GetLocation(self):
    '''Get the location of this Presence message.

    Returns:
      The location of this Presence message.
    '''    
    return self._location
    
  def SetLocation(self, location):
    '''Set the location of this Presence message.

    Args:
      location: The location of this Presence message
    '''
    self._location = location
  
  content = property(GetLocation, SetLocation,
                    doc='The location of this presence.')


  def __ne__(self, other):
    return not self.__eq__(other)

  def __eq__(self, other):
    try:
      return other and \
             self.created_at == other.created_at and \
             self.id == other.id and \
             self.title == other.title and \
             self.content == other.content and \
             self.pretty_content == other.pretty_content and \
             self.user == other.user and \
             self.created_at_relate == other.created_at_relative and \
             self.location == other.location and \
             self.icon == other.icon and \
             self.url == other.url and \
             self.comments == other.comments
    except AttributeError:
      return False

  def __str__(self):
    '''A string representation of this jaiku.Presence instance.

    The return value is the same as the JSON string representation.

    Returns:
      A string representation of this jaiku.Presence instance.
    '''
    return self.AsJsonString()

  def AsJsonString(self):
    '''A JSON string representation of this jaiku.Presence instance.

    Returns:
      A JSON string representation of this jaiku.Presence instance
   '''
    return simplejson.dumps(self.AsDict(), sort_keys=True)

  def AsDict(self):
    '''A dict representation of this jaiku.Presence instance.

    The return value uses the same key names as the JSON representation.

    Return:
      A dict representing this jaiku.Presence instance
    '''
    data = {}
    if self.created_at:
      data['created_at'] = self.created_at
    if self.id:
      data['id'] = self.id
    if self.title:
      data['title'] = self.title
    if self.content:
      data['content'] = self.content
    if self.pretty_content:
      data['pretty_content'] = self.pretty_content
    if self.user:
      data['user'] = self.user.AsDict()
    if self.created_at_relative:
      data['created_at_relative'] = self.created_at_relative
    if self.icon:
      data['icon'] = self.icon
    if self.comments:
      data['comments'] = self.comments
    if self.url:
      data['url'] = self.url
    if self.location:
      data['location'] = self.location
    return data

  @staticmethod
  def NewFromJsonDict(data):
    '''Create a new instance based on a JSON dict.

    Args:
      data: A JSON dict, as converted from the JSON in the Jaiku API
    Returns:
      A jaiku.Presence instance
    '''
    if 'user' in data:
      user = User.NewFromJsonDict(data['user'])
    else:
      user = None
    return Presence(created_at=data.get('created_at', None),
                  id=data.get('id', None),
                  comment_id=data.get('comment_id', None),
                  title=data.get('title', None),
                  content=data.get('content', None),
                  pretty_content=data.get('pretty_content', None),
                  created_at_relative=data.get('created_at_relative', None),
                  comments=data.get('comments', None),
                  icon=data.get('icon', None),
                  location=data.get('location', None),
                  url=data.get('url', None),
                  user=user)


class User(object):
  '''A class representing the User structure used by the jaiku API.

  The User structure exposes the following properties:

    user.avatar
    user.first_name
    user.last_name
    user.nick
    user.url
    user.Presence
  '''
  def __init__(self,
               avatar=None,
               first_name=None,
               last_name=None,
               nick=None,
               url=None):
    self.avatar = avatar
    self.first_name = first_name
    self.last_name = last_name
    self.nick = nick
    self.url = url

  def GetFirstName(self):
    '''Get the real name of this user.

    Returns:
      The real name of this user
    '''
    return self._first_name

  def SetFirstName(self, first_name):
    '''Set the real name of this user.

    Args:
      name: The real name of this user
    '''
    self._first_name = first_name

  name = property(GetFirstName, SetFirstName,
                  doc='The real name of this user.')

  def GetLastName(self):
    '''Get the first name of this user.

    Returns:
      The first name of this user
    '''
    return self._last_name

  def SetLastName(self, last_name):
    '''Set the short username of this user.

    Args:
      last_name: the last name of this user
    '''
    self._last_name = last_name

  screen_name = property(GetLastName, SetLastName,
                         doc='The last name of this user.')

  def GetLocation(self):
    '''Get the geographic location of this user.

    Returns:
      The geographic location of this user
    '''
    return self._location

  def SetLocation(self, location):
    '''Set the geographic location of this user.

    Args:
      location: The geographic location of this user
    '''
    self._location = location

  location = property(GetLocation, SetLocation,
                      doc='The geographic location of this user.')

  def GetDescription(self):
    '''Get the short text description of this user.

    Returns:
      The short text description of this user
    '''
    return self._description

  def SetDescription(self, description):
    '''Set the short text description of this user.

    Args:
      description: The short text description of this user
    '''
    self._description = description

  description = property(GetDescription, SetDescription,
                         doc='The short text description of this user.')

  def GetName(self):
    '''Returns the first name and last name in one string.'''
    return '%s %s' % ( self.first_name, self.last_name)
    
  name = property(GetName, doc='Convenience to get the full name.')

  def GetUrl(self):
    '''Get the homepage url of this user.

    Returns:
      The homepage url of this user
    '''
    return self._url

  def SetUrl(self, url):
    '''Set the homepage url of this user.

    Args:
      url: The homepage url of this user
    '''
    self._url = url

  url = property(GetUrl, SetUrl,
                 doc='The homepage url of this user.')

  def GetAvatar(self):
    '''Get the url of the thumbnail of this user.

    Returns:
      The url of the thumbnail of this user
    '''
    return self._avatar

  def SetAvatar(self, avatar):
    '''Set the url of the thumbnail of this user.

    Args:
      profile_image_url: The url of the thumbnail of this user
    '''
    self._avatar = avatar

  profile_image_url= property(GetAvatar, SetAvatar,
                              doc='The avatar of this user.')

  def __ne__(self, other):
    return not self.__eq__(other)

  def __eq__(self, other):
    try:
      return other and \
             self.avatar == other.avatar and \
             self.first_name == other.first_name and \
             self.last_name == other.last_name and \
             self.nick == other.nick and \
             self.url == other.url
    except AttributeError:
      return False

  def __str__(self):
    '''A string representation of this jaiku.User instance.

    The return value is the same as the JSON string representation.

    Returns:
      A string representation of this jaiku.User instance.
    '''
    return self.AsJsonString()

  def AsJsonString(self):
    '''A JSON string representation of this jaiku.User instance.

    Returns:
      A JSON string representation of this jaiku.User instance
   '''
    return simplejson.dumps(self.AsDict(), sort_keys=True)

  def AsDict(self):
    '''A dict representation of this jaiku.User instance.

    The return value uses the same key names as the JSON representation.

    Return:
      A dict representing this jaiku.User instance
    '''
    data = {}
    if self.avatar:
      data['avatar'] = self.avatar
    if self.first_name:
      data['first_name'] = self.first_name
    if self.last_name:
      data['last_name'] = self.last_name
    if self.nick:
      data['nick'] = self.nick
    if self.url:
      data['url'] = self.url
    return data

  @staticmethod
  def NewFromJsonDict(data):
    '''Create a new instance based on a JSON dict.

    Args:
      data: A JSON dict, as converted from the JSON in the jaiku API
    Returns:
      A jaiku.User instance
    '''
    return User(avatar=data.get('avatar', None),
                first_name=data.get('first_name', None),
                last_name=data.get('last_name', None),
                nick=data.get('nick', None),
                url=data.get('url', None),
                )

class Api(object):
  '''A python interface into the Jaiku API, blatantly stolen from
  DeWitt Clinton's Twitter API

  By default, the Api caches results for 1 minute.

  Example usage:

    To create an instance of the jaiku.Api class, with no authentication:

      >>> import jaiku
      >>> api = jaiku.Api()

    To fetch a single user's public Presences, where "user" is
    a Jaiku name.

      >>> presences = api.GetUserFeed(name)
      >>> print [s.title for s in presences]

    To fetch a user's friends:

      >>> users = api.GetContacts(user)
      >>> print [u.name for u in users]

    To use authentication, instantiate the jaiku.Api class with a
    username and api key (obtainable from http://api.jaiku.com):

      >>> api = jaiku.Api(username='username', api_key='jaiku api key')

    To post a new jaiku Presence (after being authenticated):

      >>> Presence = api.PostPresence('I love python-jaiku!')
      >>> print Presence.text
      I love python-jaiku!

    There are many other methods, including:
      >>> api.GetLatest(user)
      >>> api.GetUser(user)
      >>> api.GetUserTimeline(user)
      >>> api.GetContactsFeed(user)
      >>> api.GetContacts(user)
  '''

  DEFAULT_CACHE_TIMEOUT = 60 # cache for 1 minute

  _API_REALM = 'Jaiku API'

  def __init__(self, username=None, api_key=None, request_headers=None):
    '''Instantiate a new jaiku.Api object.

    Args:
      username: The username of the jaiku account.  [optional]
      api_key: The api key for the jaiku account (at http://api.jaiku.com). [optional]
    '''
    self._cache = _FileCache()
    self._urllib = urllib2
    self._cache_timeout = Api.DEFAULT_CACHE_TIMEOUT
    self._InitializeRequestHeaders(request_headers)
    self._InitializeUserAgent()
    self.SetCredentials(username, api_key)

  def GetPublicFeed(self):
    '''Fetch the sequnce of public jaiku.Presence message for all users.

    Returns:
      An sequence of jaiku.Presence instances, one for each message
    '''
    parameters = {}
    if self._username and self._api_key:
      parameters['username'] = self._username
      parameters['personal_key'] = self._api_key
    url = 'http://jaiku.com/feed/json'
    json = self._FetchUrl(url,  parameters=parameters)
    data = simplejson.loads(json)['stream']
    return [Presence.NewFromJsonDict(x) for x in data]

  def GetContactsFeeds(self):
    '''Fetch the latest updates from your contacts feed.  Returns jaiku.Presence
       for Presence *and comment* in the feed.
       
       Returns:
         An sequence of jaiku.Presence instances, one for each message and one 
         for each comment. '''
    if not self._username and not self._api_key:
      raise JaikuException("You must be authenticated for this.")
    parameters = {}
    parameters['user'] = self._username
    parameters['personal_key'] = self._api_key
    url = 'http://%s.jaiku.com/contacts/feed/json' % self._username
    json = self._FetchUrl(url, parameters=parameters)
    data = simplejson.loads(json)['stream']
    return [Presence.NewFromJsonDict(x) for x in data]

  def GetUserFeed(self, user=None, count=None):
    '''Fetch the sequence of public jaiku.Presence messages for a single user.

    The jaiku.Api instance must be authenticated if the user is private.

    Args:
      user:
        the username of the user to retrieve.  If
        not specified, then the current authenticated user is used. [optional]
      count: the number of Presence messages to retrieve [optional]

    Returns:
      A sequence of jaiku.Presence instances, one for each message up to count
    '''
    try:
      if count:
        int(count)
    except:
      raise JaikuException("Count must be an integer")
    parameters = {}
    if user:
      url = 'http://%s.jaiku.com/feed/json' % user
    elif not user and not self._username:
      raise JaikuException("User must be specified if API is not authenticated.")
    else:
      url = 'http://%s.jaiku.com/feed/json' % self._username
    if self._username and self._api_key:
      parameters['user'] = self._username
      parameters['personal_key'] = self._api_key
    json = self._FetchUrl(url, parameters=parameters)
    data = simplejson.loads(json)['stream']
    if count:
      return [Presence.NewFromJsonDict(x) for x in data[:count]]
    else:
      return [Presence.NewFromJsonDict(x) for x in data]

  def GetLatest(self, user=None):
    '''Fetch the sequence of public jaiku.Presence messages for a single user.

    The jaiku.Api instance must be authenticated if the user is private.

    Args:
      user:
        the username the user to retrieve.  If
        not specified, then the current authenticated user is used. [optional]

    Returns:
      A jaiku.Presence instance
    '''

    parameters = {}
    if user:
      url = 'http://%s.jaiku.com/presence/last/json' % user
    elif not user and not self._username:
      raise JaikuException("User must be specified if API is not authenticated.")
    else:
      url = 'http://%s.jaiku.com/presence/last/json' % self._username
    if self._username and self._api_key:
      parameters['user'] = self._username
      parameters['personal_key'] = self._api_key
    json = self._FetchUrl(url, parameters=parameters)
    data = simplejson.loads(json)
    return Presence.NewFromJsonDict(data)

  def GetChannelFeed(self, channel=None, count=None):
    '''Fetch the sequence of public jaiku.Presence messages for a Jaiku channel.

    Args:
      user:
        The channel name of the channel to retrieve
        count: the number of Presence messages to retrieve [optional]

    Returns:
      A sequence of jaiku.Presence instances, one for each message up to count
    '''
    try:
      if count:
        int(count)
    except:
      raise JaikuException("Count must be an integer")
    parameters = {}
    if channel:
      url = 'http://jaiku.com/channel/%s/feed/json' % channel
    else:
      raise JaikuException("You must provide a channel to grab the feed from.")
    if self._username and self._api_key:
      parameters['user'] = self._username
      parameters['personal_key'] = self._api_key
    json = self._FetchUrl(url, parameters=parameters)
    data = simplejson.loads(json)['stream']
    if count:
      return [Presence.NewFromJsonDict(x) for x in data[:count]]
    else:
      return [Presence.NewFromJsonDict(x) for x in data]

  def GetPresence(self, user, id):
    '''Returns a single Presence message.

    The jaiku.Api instance must be authenticated if the Presence message is private.

    Args:
      id: The numerical ID of the Presence you're trying to retrieve.

    Returns:
      A jaiku.Presence instance representing that Presence message
    '''
    try:
      if id:
        int(id)
    except:
      raise JaikuException("id must be an integer")
    if user:
      url = 'http://%s.jaiku.com/Presence/%s/json' % ( user, id )
    elif not user and not self._username:
      raise JaikuException("User must be specified if API is not authenticated.")
    else:
      url = 'http://%s.jaiku.com/Presence/%s/json' % ( self._username, id)
    json = self._FetchUrl(url)
    data = simplejson.loads(json)
    return Presence.NewFromJsonDict(data)

  def PostPresence(self, text, location=None, icon=None, generated=False):
    '''Post a jaiku Presence message from the authenticated user.

    The jaiku.Api instance must be authenticated.

    Args:
      text: The message text to be posted.  Must be less than 140 characters.
      location: Your location.  String.
      generated: whether or this is a generated post.  People don't get 
      notifications about generated posts.

    Returns:
      A jaiku.Presence instance representing the message posted
    '''
    if not self._username and not self._api_key:
      raise JaikuException("The jaiku.Api instance must be authenticated.")
    if len(text) > 140:
      raise JaikuException("Text must be less than or equal to 140 characters.")
    url = 'http://api.jaiku.com/json'
    data = {'message': text}
    if location:
      data['location'] = location
    if generated:
      data['generated'] = generated
    if icon:
      if str(icon) in ICON_DICT.values():
        data['icon'] = icon
      elif ICON_DICT.get(icon, None):
        data['icon'] = ICON_DICT[icon]
      else:
        raise JaikuException('Sorry, you have entered an invalid icon - must either be a valid integer or valid shortname.  See list here: http://code.google.com/p/python-jaiku/wiki/IconDict')
    parameters = {'user': self._username, 'personal_key': self._api_key}
    data['method'] = 'presence.send'
    json = self._FetchUrl(url, post_data=data, parameters=parameters)
    data = simplejson.loads(json)
    return data

  def GetContacts(self, user=None):
    '''Fetch the sequence of jaiku.User instances, one for each friend.

    Args:
      user: the username or id of the user whose friends you are fetching.  If
      not specified, defaults to the authenticated user. [optional]

    Returns:
      A sequence of jaiku.User instances, one for each friend
    '''
    if user:
      url = 'http://%s.jaiku.com/json' % user
    elif not user and not self._username:
      raise JaikuException("Must either be authenticated or provide a username.")
    json = self._FetchUrl(url)
    data = simplejson.loads(json)['contacts']
    return [User.NewFromJsonDict(x) for x in data]

  def GetUser(self, user):
    '''Returns a single user.

    Args:
      user: The username of the user to retrieve.

    Returns:
      A jaiku.User instance representing that user
    '''
    url = 'http://%s.jaiku.com/json' % user
    json = self._FetchUrl(url)
    data = simplejson.loads(json)
    return User.NewFromJsonDict(data)

  def SetCredentials(self, username, api_key):
    '''Set the username and api_key for this instance

    Args:
      username: The jaiku username.
      api_key: The jaiku api key from http://api.jaiku.com .
    '''
    self._username = username
    self._api_key = api_key

  def ClearCredentials(self):
    '''Clear the username and api_key for this instance
    '''
    self._username = None
    self._api_key = None

  def SetCache(self, cache):
    '''Override the default cache.  Set to None to prevent caching.

    Args:
      cache: an instance that supports the same API as the  jaiku._FileCache
    '''
    self._cache = cache

  def _InitializeRequestHeaders(self, request_headers):
    if request_headers:
      self._request_headers = request_headers
    else:
      self._request_headers = {}

  def SetUrllib(self, urllib):
    '''Override the default urllib implementation.

    Args:
      urllib: an instance that supports the same API as the urllib2 module
    '''
    self._urllib = urllib

  def SetCacheTimeout(self, cache_timeout):
    '''Override the default cache timeout.

    Args:
      cache_timeout: time, in seconds, that responses should be reused.
    '''
    self._cache_timeout = cache_timeout

  def SetUserAgent(self, user_agent):
    '''Override the default user agent

    Args:
      user_agent: a string that should be send to the server as the User-agent
    '''
    self._request_headers['User-Agent'] = user_agent

  def _BuildUrl(self, url, path_elements=None, extra_params=None):
    # Break url into consituent parts
    (scheme, netloc, path, params, query, fragment) = urlparse.urlparse(url)

    # Add any additional path elements to the path
    if path_elements:
      # Filter out the path elements that have a value of None
      p = [i for i in path_elements if i]
      if not path.endswith('/'):
        path += '/'
      path += '/'.join(p)

    # Add any additional query parameters to the query string
    if extra_params and len(extra_params) > 0:
      extra_query = self._EncodeParameters(extra_params)
      # Add it to the existing query
      if query:
        query += '&' + extra_query
      else:
        query = extra_query

    # Return the rebuilt URL
    return urlparse.urlunparse((scheme, netloc, path, params, query, fragment))

  def _InitializeRequestHeaders(self, request_headers):
    if request_headers:
      self._request_headers = request_headers
    else:
      self._request_headers = {}

  def _InitializeUserAgent(self):
    user_agent = 'Python-urllib/%s (python-jaiku/%s)' % \
                 (self._urllib.__version__, jaiku.__version__)
    self.SetUserAgent(user_agent)

  def _GetOpener(self, url, username=None, api_key=None):
    opener = self._urllib.build_opener()
    opener.addheaders = self._request_headers.items()
    return opener

  def _EncodeParameters(self, parameters):
    '''Return a string in key=value&key=value form

    Values of None are not included in the output string.

    Args:
      parameters:
        A dict of (key, value) tuples, where value is encoded as
        specified by self._encoding
    Returns:
      A URL-encoded string in "key=value&key=value" form
    '''
    if parameters is None:
      return None
    else:
      return urllib.urlencode(dict([(k, v) for k, v in parameters.items() if v is not None]))  

  def _EncodePostData(self, post_data):
    '''Return a string in key=value&key=value form

    Args:
      post_data:
        A dict of (key, value) tuples
    Returns:
      A URL-encoded string in "key=value&key=value" form
    '''
    if post_data is None:
      return None
    if not self._username or not self._api_key:
      raise JaikuException("This method requires a valid username and api key.")
    else:
      post_data['user'] = self._username
      post_data['api_key'] = self._api_key
      return urllib.urlencode(post_data)

  def _FetchUrl(self,
                url,
                post_data=None,
                parameters=None,
                no_cache=None):
    '''Fetch a URL, optionally caching for a specified time.

    Args:
      url: The URL to retrieve
      data: A dict of (str, unicode) key value pairs.  If set, POST will be used.
      parameters: A dict of key/value pairs that should added to
                  the query string. [OPTIONAL]
      username: A HTTP Basic Auth username for this request
      username: A HTTP Basic Auth api_key for this request
      no_cache: If true, overrides the cache on the current request

    Returns:
      A string containing the body of the response.
    '''
    # Add key/value parameters to the query string of the url
    url = self._BuildUrl(url, extra_params=parameters)
  
    opener = self._GetOpener(url, username=self._username, api_key=self._api_key)

    encoded_post_data = self._EncodePostData(post_data)
    
    # Open and return the URL immediately if we're not going to cache
    if encoded_post_data or no_cache or not self._cache or not self._cache_timeout:
      url_data = opener.open(url, encoded_post_data).read()
    else:
      # Unique keys are a combination of the url and the username
      if self._username:
        key = self._username + ':' + url
      else:
        key = url

      # See if it has been cached before
      last_cached = self._cache.GetCachedTime(key)

      # If the cached version is outdated then fetch another and store it
      if not last_cached or time.time() >= last_cached + self._cache_timeout:
        url_data = opener.open(url, encoded_post_data).read()
        self._cache.Set(key, url_data)
      else:
        url_data = self._cache.Get(key)

    # Always return the latest version
    return url_data

class _FileCacheError(Exception):
  '''Base exception class for FileCache related errors'''

class _FileCache(object):

  DEPTH = 3

  def __init__(self,root_directory=None):
    self._InitializeRootDirectory(root_directory)

  def Get(self,key):
    path = self._GetPath(key)
    if os.path.exists(path):
      return open(path).read()
    else:
      return None

  def Set(self,key,data):
    path = self._GetPath(key)
    directory = os.path.dirname(path)
    if not os.path.exists(directory):
      os.makedirs(directory)
    if not os.path.isdir(directory):
      raise _FileCacheError('%s exists but is not a directory' % directory)
    temp_fd, temp_path = tempfile.mkstemp()
    temp_fp = os.fdopen(temp_fd, 'w')
    temp_fp.write(data)
    temp_fp.close()
    if not path.startswith(self._root_directory):
      raise _FileCacheError('%s does not appear to live under %s' %
                            (path, self._root_directory))
    if os.path.exists(path):
      os.remove(path)
    os.rename(temp_path, path)

  def Remove(self,key):
    path = self._GetPath(key)
    if not path.startswith(self._root_directory):
      raise _FileCacheError('%s does not appear to live under %s' %
                            (path, self._root_directory ))
    if os.path.exists(path):
      os.remove(path)

  def GetCachedTime(self,key):
    path = self._GetPath(key)
    if os.path.exists(path):
      return os.path.getmtime(path)
    else:
      return None

  def _GetUsername(self):
    '''Attempt to find the username in a cross-platform fashion.'''
    return os.getenv('USER') or \
        os.getenv('LOGNAME') or \
        os.getenv('USERNAME') or \
        os.getlogin() or \
        'nobody'

  def _GetTmpCachePath(self):
    username = self._GetUsername()
    cache_directory = 'python.cache_' + username
    return os.path.join(tempfile.gettempdir(), cache_directory)

  def _InitializeRootDirectory(self, root_directory):
    if not root_directory:
      root_directory = self._GetTmpCachePath()
    root_directory = os.path.abspath(root_directory)
    if not os.path.exists(root_directory):
      os.mkdir(root_directory)
    if not os.path.isdir(root_directory):
      raise _FileCacheError('%s exists but is not a directory' %
                            root_directory)
    self._root_directory = root_directory

  def _GetPath(self,key):
    hashed_key = md5.new(key).hexdigest()
    return os.path.join(self._root_directory,
                        self._GetPrefix(hashed_key),
                        hashed_key)

  def _GetPrefix(self,hashed_key):
    return os.path.sep.join(hashed_key[0:_FileCache.DEPTH])