from flask.ext import login

from wtforms import form, fields, validators

from studsrv.frontend.utils import TemplateView, FormView, ActionView

from studsrv.services.image import images
from studsrv.services.project import projects



class UserTemplateMixin(object):
  @property
  def projects(self):
    return list(projects.getProjectsForUser(username = login.current_user.id))



class IndexView(UserTemplateMixin,
                TemplateView):
  template = 'user/index.html'



class ProjectCreateView(UserTemplateMixin,
                        FormView):
  template = 'user/project/create.html'
  
  
  class form_class(form.Form):
    # TODO: Validate names uniqueness
    name = fields.TextField('Name',
                            validators = [validators.Length(min = 1, max = 63),
                                          validators.Regexp(r'^([a-zA-Z0-9_\-])+$')],
                            description = '''Der Name deines Projekts - der Name
                                             wird verwendet, um das Projekt
                                             aufzurufen und darf nur aus
                                             Buchstaben und Zahlen bestehen''')
    
    image = fields.RadioField('Typ',
                              choices = [(image.name, image.title)
                                         for image
                                         in (images.getImage(name = name)
                                             for name
                                             in images.getImages())],
                              description = '''Der Typ des Projekts bestimmt,
                                               welche Funktionen in dem Projekt
                                               zur Verfügung stehen''')
    
    description = fields.TextAreaField('Beschreibung',
                                       description = '''Eine kurze Beschreibung
                                                        deines Projektes - die
                                                        Beschreibung wird in der
                                                        Liste der Projekte
                                                        angezeigt''')
    
    public = fields.BooleanField('Öffentlich',
                                 description = '''Nicht-öffentliche Projekte
                                                  sind nur von den Computern der
                                                  Hochschule Fulda aus
                                                  aufrufbar, öffentliche
                                                  hingegen sind im gesammten
                                                  Internet aufrufbar -
                                                  öffentliche Projekte müssen
                                                  öfters überprüft und
                                                  aktuallisiert werden''')
  
  
  def valid(self,
            name,
            image,
            description,
            public):
    projects.createProject(username = login.current_user.id,
                           name = name,
                           image = image,
                           description = description,
                           public = public)
    
    return self.url('user.project.details',
                    name = name)



class ProjectTemplateMixin(object):
  @property
  def project(self):
    return projects.getProjectForUser(username = login.current_user.id,
                                      name = self.name)



class ProjectDetailsView(UserTemplateMixin,
                         ProjectTemplateMixin,
                         TemplateView):
  template = 'user/project/details.html'



class ProjectStartView(ProjectTemplateMixin,
                       ActionView):
  def do(self):
    self.project.start()
    
    return self.url('user.project.details',
                    name = self.name)



class ProjectStopView(ProjectTemplateMixin,
                      ActionView):
  def do(self):
    self.project.stop()
    
    return self.url('user.project.details',
                    name = self.name)



class ProjectDeleteView(ProjectTemplateMixin,
                        ActionView):
  def do(self):
    self.project.delete()
    
    return self.url('user.index',
                    name = self.name)



class ProjectAddAdminView(ProjectTemplateMixin,
                          ActionView):
  def do(self):
    # TODO: Pass in username to add
    self.project.addAdmin(username = None)
    
    return self.url('user.project.details',
                    name = self.name)



class ProjectRemoveAdminView(ProjectTemplateMixin,
                             ActionView):
  def do(self):
    self.project.removeAdmin(username = login.current_user.id)
    
    return self.url('user.index')
    