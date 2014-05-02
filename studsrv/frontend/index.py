from flask.ext import login

from wtforms import form, fields, validators

from studsrv.frontend.utils import TemplateView, FormView, ActionView
from studsrv.services.user import users
  


class IndexView(TemplateView):
  template = 'index.html'
  


class LoginView(FormView):
  template = 'login.html'
  
  
  class form_class(form.Form):
    username = fields.TextField(validators = [validators.Length(min = 1, max = 255)])
    
    password = fields.TextField()
    
    remember = fields.BooleanField()
    
    def validate_password(self, field):
      if not users.authenticateUser(username = self.username.data,
                                    password = self.password.data):
        raise validators.ValidationError('Benutzname oder Passwort falsch')
  
  
  def valid(self,
            username,
            password,
            remember):
    # Get the user instance
    user = users.getUser(username = username)
    
    # Login
    login.login_user(user = user,
                     remember = remember)
    
    return self.url('user.index')



class LogoutView(ActionView):
  def do(self):
    login.logout_user()
    
    return self.url('index')
    