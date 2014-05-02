from django.views.generic import TemplateView, RedirectView
from django.views.generic.edit import FormView
from django.core import urlresolvers

from studsrv.api.services import images, projects
from studsrv.frontend.forms import AddProjectForm



class BaseMixin(object):
  
  @property
  def projects(self):
    # TODO: Pass user
    return projects.getProjectsForUser(None)



class IndexView(BaseMixin, TemplateView):
  template_name = 'studsrv/frontend/index.html'



class ProjectCreateView(BaseMixin, FormView):
  template_name = 'studsrv/frontend/project_create.html'
  form_class = AddProjectForm
  
  
  def get_success_url(self):
    return urlresolvers.reverse('studsrv.frontend.project.details',
                                kwargs = self.kwargs)
  
  
  def form_valid(self, form):
    projects.createProject(name = form.cleaned_data['name'],
                           image_id = form.cleaned_data['image'],
                           description = form.cleaned_data['description'])
    
    return FormView.form_valid(self, form)
  
  

class ProjectMixin(object):
  
  @property
  def name(self):
    return self.kwargs['name']
  
  
  @property
  def project(self):
    return projects.getProjectInfo(self.name)



class ProjectDetailsView(BaseMixin, ProjectMixin, TemplateView):
  template_name = 'studsrv/frontend/project_details.html'



class ProjectStartView(ProjectMixin, RedirectView):
  pattern_name = 'studsrv.frontend.project.details'
  
  
  def post(self, request, *args, **kwargs):
    projects.startProject(self.name)
    
    return super(ProjectStartView, self).post(request, *args, **kwargs)



class ProjectStopView(ProjectMixin, RedirectView):
  pattern_name = 'studsrv.frontend.project.details'
  
  
  def post(self, request, *args, **kwargs):
    projects.stopProject(self.name)
    
    return super(ProjectStopView, self).post(request, *args, **kwargs)
  
  
