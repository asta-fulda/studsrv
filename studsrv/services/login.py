import logging
import os.path

from flask.ext import login

from sh import btrfs

from studsrv.services.config import configs



class User(login.UserMixin):
  def __init__(self,
               username):
    self.__username = username

    # TODO: Fetch LDAP response

    # Ensure the users subvolume exist
    if not os.path.isdir(self.volume):
      btrfs.subvolume.create(self.volume)

      logging.warning('User volume created: %s', self.volume)
  
  
  @property
  def id(self):
    return self.__username


  @property
  def email(self):
    ''' Returns the email address of the user.
    '''

    # TODO: Get from LDAP
    pass


  @property
  def name(self):
    ''' Returns the full name of the user.
    '''

    # TODO: Get from LDAP
    pass


  @property
  def volume(self):
    ''' Returns the path to the users volume.
    '''

    return os.path.join(configs.users_volume,
                        self.id)
    
  

class LoginService(object):
  def __init__(self):
    self.__login_manager = login.LoginManager()
  
  
  def initApplication(self, app):
    @self.__login_manager.user_loader
    def get_user(username):
      return self.getUser(username = username)
    
    self.__login_manager.login_view = 'login'
    
    self.__login_manager.init_app(app)


  def authenticateUser(self,
                       username,
                       password):
    # TODO: Check against LDAP
    if username != password:
      return False

    return True
    
    
  def getUser(self,
              username):
    # TODO: Get from LDAP
    return User(username = username)


logins = LoginService()
