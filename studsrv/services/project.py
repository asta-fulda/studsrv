import os.path
from datetime import datetime
import pytz

try:
  from sh import btrfs
except:
  from sh import echo as btrfs

import docker

from studsrv import db



client = docker.Client(version='1.9')



class ConfigService(object):
  def __init__(self):
    pass
  
  
  def __getattr__(self, name):
    # TODO lookup in application configuration
    if name == 'projects_volume':
      return '/mnt/projects'
    
    if name == 'projects_hostname_pattern':
      return '%s.stud-new.hs-fulda.org'
    
    if name == 'project_url_pattern':
      return 'http://%s.stud-new.hs-fulda.org'
    
    if name == 'project_quota':
      return '1g'
    
    raise None


configs = ConfigService()



class Project(object):
  def __init__(self,
               record):
    self.__record = record
    
    self.__container = client.inspect_container(container = self.__record.container_id)
  
  
  @property
  def name(self):
    return self.__record.name
  
  
  @property
  def image(self):
    return self.__record.image
  
  
  @property
  def description(self):
    return self.__record.description
  
  
  @property
  def created(self):
    return self.__record.created
  
  
  @property
  def enabled(self):
    return self.__record.enabled
  
  
  @property
  def blocked(self):
    return self.__record.blocked
    
  
  @property
  def url(self):
    return configs.project_url_pattern % self.name
  
  
  @property
  def public(self):
    return self.__record.public
  
  
  @property
  def running(self):
    return self.__container['State']['Running']
  
  
  @property
  def started(self):
    print(self.__container['State']['StartedAt'])
    return datetime.strptime(self.__container['State']['StartedAt'][:26],
                             '%Y-%m-%dT%H:%M:%S.%f').replace(tzinfo = pytz.utc).astimezone(None)
  
  
  @property
  def uptime(self):
    return datetime.now(tz = pytz.utc) - self.started



class ProjectService(object):
  def __project_volume(self,
                     name):
    return os.path.join(configs.projects_volume,
                        name)
  
  
  def __project_hostname(self,
                         name):
    return configs.projects_hostname_pattern % name
  
  
  def createProject(self,
                    name,
                    image,
                    description,
                    public):
    # Remove an maybe existing project subvolue
    if os.path.isdir(self.__project_volume(name)):
      btrfs.subvolume.delete(self.__project_volume(name))
    
    # Create the projects subvolume
    btrfs.subvolume.create(self.__project_volume(name))
    
    # TODO: Set the quota for the projects subvolume
    btrfs.qgroup.limit(configs.project_quota,
                       self.__project_volume(name))

    
    # Create a container for the project
    container_id = client.create_container(image = image,
                                           hostname = self.__project_hostname(name),
                                           name = name,
                                           volumes = {'/data': {}})['Id']
    
    project = db.Project(name = name,
                         image = image,
                         description = description,
                         public = public,
                         container_id = container_id)
    
    db.session.add(project)
    db.session.commit()
  
  
  def getProjectsForUser(self,
                         user):
    for record in db.Project.query.all():
      yield record.name
  
  
  def getProjectByName(self,
                       name):
    record = db.Project.query.get(name)
    return Project(record)
  
  
  def startProject(self,
                   name):
    record = db.Project.query.get(name)
    
    # Start the container
    # TODO: Recreate the container if required
    client.start(container = record.container_id,
                 binds = {self.__project_volume(name): '/data'})
    
    # Mark the project as enabled
    record.enabled = True
    
    db.session.commit()
  
  
  def stopProject(self,
                  name):
    record = db.Project.query.get(name)
    
    # Stop the container
    client.stop(container = record.container_id)
    
    # Mark the project as disabled
    record.enabled = False
    
    db.session.commit()


projects = ProjectService()
