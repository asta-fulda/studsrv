from django.db import models

import os.path
import docker



client = docker.Client()



class Image(models.Model):
  name = models.SlugField(primary_key = True,
                          default = None,
                          max_length = 256)
  
  title = models.CharField(default = None,
                          max_length = 256)

  description = models.TextField()

  image = models.CharField(default = None,
                           max_length = 256)


  def __unicode__(self):
      return self.name



# TODO: Add expires field
class Project(models.Model):
  name = models.SlugField(primary_key = True,
                          default = None,
                          max_length = 63)  # Length as specified by DNS name part

  image = models.ForeignKey(Image)

  description = models.TextField(blank = True)

  created = models.DateTimeField(auto_now_add = True)
  
  enabled = models.BooleanField(default = True)

  blocked = models.TextField(null = True,
                             default = None)


  def __unicode__(self):
    return self.name
  
  
  def create(self):
    os.mkdir(self.volume)
    
    client.create_container(image = self.image.image,
                            hostname = self.name,
                            network_disabled = False,
                            name = self.container,
                            volumes = {'/data': {}})
  
  
  def destroy(self):
    client.remove_container(container = self.container,
                            v = True)
  
  
  def start(self):
    client.start(container = self.container,
                 binds = {self.volume: '/data'})
  
  
  def stop(self):
    client.stop(container = self.container)


  @property
  def container(self):
    return '%s.stud' % self.name


  @property
  def volume(self):
    return os.path.join('/mnt/projects', self.name)


  @property
  def running(self):
    try:
      return client.inspect_container(container = self.container)['State']['Running']
    except:
      return False


  @property
  def url(self):
    return 'http://%s.stud-new.hs-fulda.org' % self.name
