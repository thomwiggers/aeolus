#! /usr/bin/env python
#
# A more advanced IRC bot
#
# Thom Wiggers <thom@thomwiggers.nl>

import irc.client
import irc.logging
from _version import version as __version__

class AeolusBot(irc.client.IRC):

  def __init__(self):
    super(AeolusBot,self).__init__()
    self._servers = {}
    self._default_username = 'Aeolus'
    self._default_realname = 'Aeolus ' + __version__

  def connect(self, server_name, hostname, port=6667, nickname='Aeolus',password=None,
      username=None, realname=None):
    """
    Connect to a server.

    Raises AlreadyConnectedError if already connected
    """

    #Let's catch some of these problems like REALLY early
    assert isinstance(server_name, str)
    assert isinstance(port, int)
    assert isinstance(nickname, str)
    assert password is None or isinstance(password, str)
    assert username is None or isinstance(username, str)
    assert realname is None or isinstance(realname, str)

    if server_name in self._servers and 'server' in self._servers[server_name]:
      raise AlreadyConnectedError()

    username = username or self._default_username
    realname = realname or self._default_realname

    #create a new server object
    server = self.server()
    server.connect(hostname, port, nickname, password, username, realname)

    self._servers[server_name] = {'server':server}

  def register_module(self, server_name, module):
    "Register a module with a server"
    if not server_name in self._servers:
      self._servers[server_name] = {}
    if not 'modules' in self._servers[server_name]:
      self._servers[server_name]['modules'] = {}

    if module.__name__ in self._servers[server_name]['modules']:
      raise ModuleAlreadyRegisteredError()

    self._servers[server_name]['modules'][module.__name__] = module(self)

  def get_module(self, server_name, module_name):
    "Gets a module instance from a server"
    try:
      return self._servers[server_name]['modules'][module_name]
    except KeyError:
      raise ModuleNotFoundError()

  def reload_module(self, server_name, module_name):
    "Reloads a module instance from a server"
    try:
      module = self._servers[server_name]['modules'][module_name]
      if hasattr(module, 'reload') and callable(module.reload):
        module.reload()
      else:
        if hasattr(module, 'destroy') and callable(module.destroy):
          module.destroy()
        self._servers[server_name]['modules'][module_name] = module.__class__(self)
    except KeyError:
      raise ModuleNotFoundError()

  def set_default_username(self, username):
    "Set the default username"
    self._default_username = username

  def set_default_realname(self, realname):
    "Sets the default realname"
    self._default_realname = realname

class AeolusError(irc.client.IRCError):
  "An error occured in the Aeolus library"

class AlreadyConnectedError(AeolusError):
  "You're already connected to this server"

class ModuleAlreadyRegisteredError(AeolusError):
  "This module is already registered. Why don't you try to reload it?"

class ModuleNotFoundError(AeolusError):
  "Module Not Found"

if __name__ == '__main__':
  pass




# vim: set ts=4 sw=2 tw=0 et :
