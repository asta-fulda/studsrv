from flask.views import View
from flask import render_template
from flask import url_for, request, redirect
from flask.ext import login



class ViewMixin(object):
  def url(self,
          endpoint,
          **values):
    return url_for(endpoint,
                   **values)
  
  
  def static(self,
             path):
    return url_for('static',
                   filename = path)
  
  
  @property
  def user(self):
    return login.current_user
  
  
  @property
  def authenticated(self):
    return login.current_user.is_authenticated()



class TemplateView(ViewMixin, View):
  template = None
  
  
  def dispatch_request(self,
                       **values):
    
    # Update the instance with the request values
    self.__dict__.update(values)
    
    # Render the template
    return render_template(self.template,
                           **{name : getattr(self, name)
                              for name
                              in dir(self)
                              if not name.startswith('__')})
                           


class FormView(TemplateView):
  methods = ['GET', 'POST']
  
  form_class = None
  
  
  def __init__(self, *args, **kwargs):
    self.__form = self.form_class(request.form)
    
    super(FormView, self).__init__()
  
  
  @property
  def form(self):
    return self.__form
  
  
  def valid(self,
            **values):
    pass
  
  
  def dispatch_request(self,
                       **values):
    if request.method == 'POST' and self.form.validate():
      return redirect(self.valid(**self.form.data))
    
    else:
      return super(FormView, self).dispatch_request(**values)
                           


class ActionView(ViewMixin, View):
  methods = ['GET', 'POST']
  
  
  def do(self):
    pass
  
  
  def dispatch_request(self,
                       **values):
    
    # Update the instance with the request values
    self.__dict__.update(values)
    
    return redirect(self.do())
