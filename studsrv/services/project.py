import logging
import os.path
from datetime import datetime
import pytz

from sh import btrfs

import docker

from studsrv import db

from studsrv.services.config import configs
from studsrv.services.image import images



client = docker.Client(version='1.9')



class Admin(object):
  def __init__(self,
               record):
    self.__record = record
  
  
  @property
  def username(self):
    ''' Returns the username of the user.
    '''
    
    return str(self.__record.id)
  
  
  @property
  def email(self):
    ''' Returns the email address of the user.
    '''
    
    # TODO: Get from LDAP
    pass
  
  
  @property
  def name(self):
    ''' Returns the full name of the user.
    '''
    
    # TODO: Get from LDAP
    pass
    
  
  @property
  def volume(self):
    ''' Returns the path to the users volume.
    '''
    
    return os.path.join(configs.users_volume,
                        self.username)
  



class Project(object):
  def __init__(self,
               record):
    self.__record = record
    
    if self.__record.container_id is not None:
      self.__container = client.inspect_container(container = self.__record.container_id)
  
  
  @property
  def name(self):
    ''' Returns the name of the project.
    '''
    
    return self.__record.id
  
  
  @property
  def image(self):
    ''' Returns the image name of the project.
    '''
    
    return images.getImage(name = self.__record.image)
  
  
  @property
  def description(self):
    ''' Returns the description of the project.
    '''
    
    return self.__record.description
  
  
  @property
  def created(self):
    ''' Returns the timestamp, when the project was created.
    '''
    
    return self.__record.created
  
  
  @property
  def enabled(self):
    ''' Returns True, iff the project is enabled.
    '''
    
    return self.__record.enabled
  
  
  @property
  def blocked(self):
    ''' Returns the blocking reason of None if the project is not blocked.
    '''
    
    return self.__record.blocked
    
  
  @property
  def volume(self):
    ''' Returns the path to the projects volume.
    '''
    
    return os.path.join(configs.projects_volume,
                        self.name)
    
  
  @property
  def hostname(self):
    ''' Returns the projects hostname.
    '''
    
    return configs.projects_hostname_pattern % self.name
    
  
  @property
  def url(self):
    ''' Returns the projects URL.
    '''
    
    return configs.projects_url_pattern % self.name
  
  
  @property
  def public(self):
    ''' Returns True, iff the project is public.
    '''
    
    return self.__record.public
  
  
  @property
  def running(self):
    ''' Returns True, iff the projects container is running.
    '''
    
    return self.__container['State']['Running']
  
  
  @property
  def started(self):
    ''' Returns the timestamp, when the project was started.
    '''
    
    print(self.__container['State']['StartedAt'])
    return datetime.strptime(self.__container['State']['StartedAt'][:26],
                             '%Y-%m-%dT%H:%M:%S.%f').replace(tzinfo = pytz.utc).astimezone(None)
  
  
  @property
  def uptime(self):
    ''' Returns the uptime of the project.
    '''
    
    return datetime.now(tz = pytz.utc) - self.started
  
  
  @property
  def admins(self):
    ''' Returns list of Administrators of the project.
    '''
    
    return (Admin(record)
            for record
            in self.__record.admins.values())
  
  
  def addAdmin(self,
               username):
    ''' Add the user with the given username to the list of administrators of
        this project.
    '''
    
    record = self.__record.admins[username] = db.Admin(id = username)
    
    admin = Admin(record = record)
    
    # Ensure the user subvolume does exists
    if not os.path.isdir(self.volume):
      btrfs.subvolume.create(admin.volume)
      
    # Bind the projects subvolume to the users subvolume
    os.symlink(self.volume,
               os.path.join(admin.volume,
                            self.name))
    
    db.session.commit()
    
    logging.warn('Admin added: project=%s, user=%s', self.name, username)
    
    return admin
  
  
  def removeAdmin(self,
                  username):
    ''' Remove the user with the given username from the list of administrators
        of this project.
    '''
    
    admin = Admin(record = self.__record.admins[username])
    
    # Remove the admin record from the project
    del self.__record.admins[username]
    
    # Remove the project from the users subvolume
    os.remove(os.path.join(admin.volume,
                           self.name))
    
    # After the last admin was removed from the project, delete it
    if not self.__record.admins:
      self.delete()
    
    db.session.commit()
    
    logging.warn('Admin removed: project=%s, user=%s', self.name, username)
  
  
  def start(self):
    ''' Start the project.
    '''
    
    # Start the container
    client.start(container = self.__record.container_id,
                 binds = {self.volume: '/data'})
    
    # Mark the project as enabled
    self.__record.enabled = True
    
    db.session.commit()
  
  
  def stop(self):
    ''' Stop the project.
    '''
    
    # Stop the container
    client.stop(container = self.__record.container_id)
    
    # Mark the project as disabled
    self.__record.enabled = False
    
    db.session.commit()
  
  
  def delete(self):
    ''' Deletes this project. '''
    
    # TODO: Delete all admins first
    
    # Delete the projects subvolume
    btrfs.subvolume.delete(self.volume)
    
    # Delete the container of the project
    client.remove_container(container = self.__record.container_id)
    
    # Delete the project record
    db.session.delete(self.__record)
    db.session.commit()
    
    logging.warn('Project Deleted: %s', self.name)



class ProjectService(object):
  
  def createProject(self,
                    username,
                    name,
                    image,
                    description,
                    public):
    ''' Creates a new project.
    '''
    
    # Create the project record
    record = db.Project(id = name,
                        image = image,
                        description = description,
                        public = public)
    
    project = Project(record = record)
    
    # Ensure the projects subvolume exists
    if not os.path.isdir(project.volume):
      btrfs.subvolume.create(project.volume)
    
      # Set the quota for the projects subvolume
      btrfs.qgroup.limit(configs.projects_quota,
                         project.volume)
    
    # Create a container for the project
    record.container_id = client.create_container(image = image,
                                                  hostname = project.hostname,
                                                  name = name,
                                                  volumes = {'/data': {}})['Id']
                                                  
    db.session.add(record)
    db.session.commit()
    
    project.addAdmin(username = username)
    
    logging.warn('Project created: name=%s', name)
    
    return project
  
  
  def getProjects(self,
                  username):
    ''' Returns the list of project names for the given username.
    '''
    
    for record in db.Project.query.join(db.Admin).filter(db.Admin.id == username).all():
      yield record.id
  
  
  def getProject(self,
                 username,
                 name):
    ''' Returns the project with the given name for the given username. '''
    
    record = db.Project.query.join(db.Admin).filter(db.Admin.id == username,
                                                    db.Project.id == name).one()
    
    return Project(record = record)
  
  
projects = ProjectService()
