from flask.ext import login



class User(login.UserMixin):
  def __init__(self,
               username):
    # TODO: Use LDAP response insted
    self.__username = username
  
  
  @property
  def id(self):
    return self.__username
  
  
  @property
  def username(self):
    return self.__username
  
  
  @property
  def email(self):
    # TODO: Get from LDAP
    pass
  
  
  @property
  def name(self):
    # TODO: Get from LDAP
    pass



class UserService(object):
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


users = UserService()