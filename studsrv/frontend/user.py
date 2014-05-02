from wtforms import form, fields, validators

from studsrv.frontend.utils import TemplateView, FormView, ActionView

from studsrv.services.project import projects



class UserTemplateMixin(object):
  @property
  def projects(self):
    # TODO: Pass user from session
    return list(projects.getProjectsForUser(user = None))



class IndexView(UserTemplateMixin,
                TemplateView):
  template = 'user/index.html'



class ProjectCreateView(UserTemplateMixin,
                        FormView):
  template = 'user/project/create.html'
  
  
  class form_class(form.Form):
    # TODO: Validate names uniqueness
    name = fields.TextField('Name',
                            validators = [validators.Length(min = 4, max = 63)],
                            description = '''Der Name deines Projekts - der Name
                                             wird verwendet, um das Projekt
                                             aufzurufen und darf nur aus
                                             Buchstaben und Zahlen bestehen''')
    
    image = fields.RadioField('Typ',
                              choices = [('static', 'Statische Webseite')],
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
    projects.createProject(name = name,
                           image = image,
                           description = description,
                           public = public)
    
    return self.url('user.project.details',
                    name = name)



class ProjectDetailsView(UserTemplateMixin,
                         TemplateView):
  template = 'user/project/details.html'
  
  
  @property
  def project(self):
    return projects.getProjectByName(self.name)



class ProjectStartView(ActionView):
  def do(self):
    projects.startProject(name = self.name)
    
    return self.url('user.project.details',
                    name = self.name)



class ProjectStopView(ActionView):
  def do(self):
    projects.stopProject(name = self.name)
    
    return self.url('user.project.details',
                    name = self.name)
    