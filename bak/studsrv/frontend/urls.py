from django.conf.urls import patterns, url

from studsrv.frontend import views



urlpatterns = patterns('',
  url(r'^$', views.IndexView.as_view(), name = 'studsrv.frontend.index'),
  url(r'^project/$', views.ProjectCreateView.as_view(), name = 'studsrv.frontend.project.create'),
  url(r'^project/(?P<name>\w+)/$', views.ProjectDetailsView.as_view(), name = 'studsrv.frontend.project.details'),
  url(r'^project/(?P<name>\w+)/start$', views.ProjectStartView.as_view(), name = 'studsrv.frontend.project.start'),
  url(r'^project/(?P<name>\w+)/stop$', views.ProjectStopView.as_view(), name = 'studsrv.frontend.project.stop'),
)

