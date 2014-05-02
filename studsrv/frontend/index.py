from flask.ext import login

from wtforms import form, fields, validators

from studsrv.frontend.utils import TemplateView, FormView, ActionView
from studsrv.services.login import logins
  


class IndexView(TemplateView):
  template = 'index.html'
  


class LoginView(FormView):
  template = 'login.html'
  
  
  class form_class(form.Form):
    username = fields.TextField(validators = [validators.Length(min = 1, max = 255)])
    
    password = fields.TextField()
    
    remember = fields.BooleanField()
    
    next = fields.TextField()
    
    
    def validate_password(self, field):
      if not logins.authenticateUser(username = self.username.data,
                                    password = self.password.data):
        raise validators.ValidationError('Benutzname oder Passwort falsch')
  
  
  def valid(self,
            username,
            password,
            remember,
            next):
    # Get the user instance
    user = logins.getUser(username = username)
    
    # Login
    login.login_user(user = user,
                     remember = remember)
    
    # Redirect to next url if it's provided
    if next:
      return next
    
    return self.url('user.index')



class LogoutView(ActionView):
  def do(self):
    login.logout_user()
    
    return self.url('index')
    