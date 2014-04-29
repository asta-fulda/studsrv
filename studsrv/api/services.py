import collections
import os.path
import docker
from sh import btrfs

from studsrv.api.models import Image, Project



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



class ImageService(object):
  def __init__(self):
    pass
  
  
  def registerImage(self,
                    image_id,
                    title,
                    description):
    # Ensure the image exists
    try:
      client.inspect_image(image_id)
      
    except:
      client.pull(image_id)
    
    # Create the image record
    image = Image(image_id = image_id,
                  title = title,
                  description = description)
    image.save()
  
  
  def unregisterImage(self,
                      image_id):
    # Find the image record
    image = Image.objects.get(pk = image_id)
    
    # Delete the image
    image.delete()
  
  
  def updateImage(self,
                  image_id):
    # Find the image record
    image = Image.objects.get(pk = image_id)
    
    # Update the image
    client.pull(image_id)
    
    for project in image.projects:
      # TODO: Evaluate if we have to restart all containers based on that image
      pass
    
  
  def getImages(self):
    return {image.image_id : image.title
            for image
            in Image.objects.all()}
  

images = ImageService()



class ProjectService(object):
  Info = collections.namedtuple('Info', ['name',
                                         'description',
                                         'image',
                                         'created',
                                         'running',
                                         'started',
                                         'url'])
  
  def __init__(self):
    pass
  
  
  def __project_volume(self,
                     name):
    return os.path.join(configs.projects_volume,
                        name)
  
  
  def __project_hostname(self,
                         name):
    return configs.projects_hostname_pattern % name
  
  
  def createProject(self,
                    name,
                    image_id,
                    description):
    # Remove an maybe existing project subvolue
    if os.path.isdir(self.__project_volume(name)):
      btrfs.subvolume.delete(self.__project_volume(name))
    
    # Create the projects subvolume
    btrfs.subvolume.create(self.__project_volume(name))
    
    # TODO: Set the quota for the projects subvolume
    btrfs.qgroup.limit(configs.project_quota,
                       self.__project_volume(name))

    
    # Find the image record
    image = Image.objects.get(pk = image_id)
    
    # Create a container for the project
    container_id = client.create_container(image = image.image_id,
                                           hostname = self.__project_hostname(name),
                                           name = name,
                                           volumes = {'/data': {}})['Id']
    
    # Create the database record
    project = Project(name = name,
                      image = image,
                      description = description,
                      container_id = container_id)
    project.save()
  
  
  def getProjectsForUser(self,
                         user):
    # TODO: Filter for user
    return [project.name
            for project
            in Project.objects.all()]
  
  
  def getProjectInfo(self,
                     name):
    # Find the project record
    project = Project.objects.get(pk = name)
    
    # Inspect the container
    container = client.inspect_container(container = project.container_id)
    
    # Return info structure
    return ProjectService.Info(name = name,
                               description = project.description,
                               image = project.image.title,
                               created = project.created,
                               running = container['State']['Running'],
                               started = container['State']['StartedAt'],
                               url = configs.project_url_pattern % name)
  
  
  def startProject(self,
                   name):
    # Find the project record
    project = Project.objects.get(pk = name)
    
    # Start the container
    # TODO: Recreate the container if required
    client.start(container = project.container_id,
                 binds = {self.__project_volume(name): '/data'})
    
    # Mark the project as enabled
    project.enabled = True
    project.save()
  
  
  def stopProject(self,
                  name):
    # Find the project record
    project = Project.objects.get(pk = name)
    
    # Stop the container
    client.stop(container = project.container_id)
    
    # Mark the project as disabled
    project.enabled = False
    project.save()


projects = ProjectService()
