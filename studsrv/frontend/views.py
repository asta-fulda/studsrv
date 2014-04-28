from django.views.generic import TemplateView, RedirectView
from django.views.generic.edit import CreateView
from django.core import urlresolvers

from studsrv.api.models import Project
from studsrv.frontend.forms import AddProjectForm



class BaseMixin(object):
  
  @property
  def projects(self):
    return Project.objects.all()



class IndexView(BaseMixin, TemplateView):
  template_name = 'studsrv/frontend/index.html'



class ProjectCreateView(BaseMixin, CreateView):
  template_name = 'studsrv/frontend/project_create.html'
  form_class = AddProjectForm
  
  
  def get_success_url(self):
    return urlresolvers.reverse('studsrv.frontend.project.details',
                                kwargs={'name': self.object.name})
  
  
  def form_valid(self, form):
    form.instance.create()
    
    return CreateView.form_valid(self, form)
  
  

class ProjectMixin(object):
  
  @property
  def project(self):
    return Project.objects.get(pk = self.kwargs['name'])



class ProjectDetailsView(BaseMixin, ProjectMixin, TemplateView):
  template_name = 'studsrv/frontend/project_details.html'



class ProjectStartView(ProjectMixin, RedirectView):
  pattern_name = 'studsrv.frontend.project.details'
  
  
  def post(self, request, *args, **kwargs):
    self.project.start()
    
    return super(ProjectStartView, self).post(request, *args, **kwargs)



class ProjectStopView(ProjectMixin, RedirectView):
  pattern_name = 'studsrv.frontend.project.details'
  
  
  def post(self, request, *args, **kwargs):
    self.project.stop()
    
    return super(ProjectStopView, self).post(request, *args, **kwargs)



class ProjectDeleteView(ProjectMixin, RedirectView):
  pattern_name = 'studsrv.frontend.index'
  
  
  def post(self, request, *args, **kwargs):
    self.project.stop()
    
    return super(ProjectDeleteView, self).post(request, *args, **kwargs)
  
  
