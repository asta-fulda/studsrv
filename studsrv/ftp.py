import pyftpdlib.authorizers
import pyftpdlib.handlers
import pyftpdlib.servers

from studsrv.services.config import configs
from studsrv.services.login import logins



class Authorizer(object):
  ''' The authorizer used to bind the login service to pyftpdlib.
  '''

  def validate_authentication(self, username, password, handler):
    if not logins.authenticateUser(username = username,
                                   password = password):
      raise pyftpdlib.authorizers.AuthenticationFailed('Authentication failed')


  def get_home_dir(self, username):
    ''' Use the users volume as the root directory.
    '''

    return logins.getUser(username = username).volume


  def get_msg_login(self, username):
    return 'Hi, %s' % username


  def get_msg_quit(self, username):
    return 'By, %s' % username


  def has_perm(self, username, perm, path = None):
    ''' Allow everything as the user is jailed to its user volume
    '''

    return 'elradfmwM'


  def impersonate_user(self, username, password):
    pass


  def terminate_impersonation(self, username):
    pass



def main():
  authorizer = Authorizer()

  handler = pyftpdlib.handlers.FTPHandler
  handler.banner = 'Welcome'
  handler.authorizer = authorizer

  server = pyftpdlib.servers.FTPServer((configs.ftp_host,
                                        int(configs.ftp_port)),
                                       handler = handler)

  server.serve_forever()



if __name__ == '__main__':
  main()
