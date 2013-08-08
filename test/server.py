import unittest
import os
import errno
import socket
import mox
from aeolus.server import Connection, ConnectionException

class ConnectionTest(unittest.TestCase):

  def setUp(self):
    """Initialises mocking objects"""
    self.mox = mox.Mox()
    #Mock sockets
    self.mock_socket = self.mox.CreateMockAnything(socket.socket)
    # hide socket.socket()
    self.mox.StubOutWithMock(socket, 'create_connection')

    self.connection = Connection()

  def tearDown(self):
    """Resets the mox stubs so we can build them again"""
    self.mox.UnsetStubs()

  def testConnectEasySuccess(self):
    """Tests connecting to a server"""
    socket.create_connection(("existingserver", 6667)).AndReturn(self.mock_socket)
    
    self.mock_socket.sendall("NICK nick\n").AndReturn(None)
    self.mock_socket.sendall("USER name host server :Thom Wiggers\n").AndReturn(None)

    #ok, en dan nu testen:
    self.mox.ReplayAll() 
    self.connection.connect("nick","existingserver")
    self.mox.VerifyAll()
    self.assertEquals("nick", self.connection.nick)

  def testConnectionFailNoSuchHost(self):
    """
    Tests failing to connect to a server because there is no host
    """
    
    socket.create_connection(("nonexistingserver", 6667)
        ).AndRaise(IOError(errno.ENOENT, os.strerror(errno.ENOENT)))
    self.mox.ReplayAll()
    with self.assertRaisesRegexp(ConnectionException, "No.*host") as ce:
      self.connection.connect("nick","nonexistingserver")
    self.mox.VerifyAll()

  def testConnectionFailTimeout(self):
    """
    Tests failing to connect due to a server timeout
    """

    socket.create_connection(("timeouthost", 6667)
        ).AndRaise(IOError(errno.ETIMEOUT, os.strerror(errno.ETIMEOUT)))
    self.mox.ReplayAll()
    with self.assertRaisesRegexp(ConnectionException, "timeout") as ce:
      self.connection.connect("nick", "timeouthost")
    self.mox.VerifyAll()

  def testConnectionFailRefused(self):
    """
    Tests failing to connect because the server refuses it
    """
    socket.create_connection(("refusehost", 6667)
      ).AndRefuse(IOError(errno.ECONNREFUSED, 
        os.strerror(errno.ECONNREFUSED)))
    self.mox.ReplayAll()
    with self.assertRaisesRegexp(ConnectionException, "refused"):
      self.connection.connect("nick", "refusehost")
    self.mox.VerifyAll()


if __name__ == "__main__":
  unittest.main()
