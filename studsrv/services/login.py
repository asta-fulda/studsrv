from flask.ext import login



class User(login.UserMixin):
  def __init__(self,
               username):
    # TODO: Use LDAP response insted
    self.__username = username
  
  
  @property
  def id(self):
    return self.__username
    
  

class LoginService(object):
  def __init__(self):
    self.__login_manager = login.LoginManager()
  
  
  def initApplication(self, app):
    @self.__login_manager.user_loader
    def get_user(username):
      return self.getUser(username = username)
    
    self.__login_manager.init_app(app)


  def authenticateUser(self,
                       username,
                       password):
    # TODO: Check against LDAP
    if username == password:
      return True
    
    else:
      return False
    
    
  def getUser(self,
              username):
    # TODO: Get from LDAP
    return User(username = username)


logins = LoginService()
