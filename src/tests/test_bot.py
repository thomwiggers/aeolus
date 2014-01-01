#!/usr/bin/env python
#
# Tests for bot.py
#
# Thom Wiggers <thom@thomwiggers.nl>

import unittest
import mock
from bot import *
import module

class AeolusBotTest(unittest.TestCase):

  @mock.patch("irc.connection.socket")
  def test_twice_connecting_fails(self,fakesock):
    bot = AeolusBot()
    bot.connect("foo","localhost")

    with self.assertRaises(AlreadyConnectedError):
      bot.connect("foo","localhost2")

  @mock.patch("irc.connection.socket")
  def test_connecting_twice_to_different_servers(self,mock):
    bot = AeolusBot()
    bot.connect("foo","foo")
    bot.connect("foobar","foobar")

  def test_register_module_twice_fails_for_same_server(self):
    bot = AeolusBot()
    bot.register_module("test", module.Module)
    with self.assertRaises(ModuleAlreadyRegisteredError):
      bot.register_module("test", module.Module)

  def test_register_module_twice_doesnt_fails_for_different_servers(self):
    bot = AeolusBot()
    bot.register_module("test", module.Module)
    bot.register_module("test2", module.Module)

  def test_get_module(self):
    bot = AeolusBot()
    bot.register_module("test", module.Module)
    fetchedModule = bot.get_module("test", module.Module.__name__)
    self.assertIs(fetchedModule.__class__, module.Module)

  def test_reload_module_with_reload_method(self):
    bot = AeolusBot()
    mymock = mock.Mock(side_effect=Exception)
    mymock.__name__ = 'fiets'
    mock2 = mock.Mock(return_value=mymock)
    mock2.__name__ = 'fiets'

    bot.register_module("test", mock2)
    bot.reload_module("test", 'fiets')
    mymock.reload.assert_called_with()
    mock2.assert_called_once_with(bot)

  def test_reload_module_without_reload_nor_destroy_method(self):
    bot = AeolusBot()
    mymock = mock.Mock(spec=module.Module)
    mymock.__name__ = 'fiets'
    mock2 = mock.Mock(spec=module.Module, return_value=mymock)
    mock2.__name__ = 'fiets'
    mymock.__class__ = mymock

    bot.register_module("test", mock2)
    bot.reload_module("test", 'fiets')
    mymock.assert_called_once_with(bot)
    mock2.assert_called_once_with(bot)

  def test_reload_module_without_reload_with_destroy(self):
    bot = AeolusBot()
    mymock = mock.Mock(spec=module.Module)
    mymock.__name__ = 'fiets'
    mock2 = mock.Mock(spec=module.Module, return_value=mymock)
    mock2.__name__ = 'fiets'
    mymock.__class__ = mymock
    mymock.attach_mock(mock.Mock(), 'destroy')

    bot.register_module("test", mock2)
    bot.reload_module("test", 'fiets')
    mymock.assert_called_once_with(bot)
    mock2.assert_called_once_with(bot)
