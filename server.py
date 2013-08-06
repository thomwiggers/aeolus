#
# Represents an irc server
#

import socket
import errno

class Connection: 

  def __init__(self):
    """Initialises the irclib"""
    pass

  def connect(self, nick, server, port=6667, alias=None, name='aeolus', realname='aeolus'):
    """
    Connects to a server on port using set nick and name.
    
    Default port is 6667
    Default alias is the server name
    Default realname and name are 'aeolus'
    """
    self.nick = nick
    try:
      self.connection = socket.create_connection((server,port))
    except IOError, e:
      if (e.errno == errno.ENOENT):
        raise ConnectionException("No such host!")
      else:
        raise e

  def disconnect(self):
    pass

class ConnectionException(Exception):
  pass
