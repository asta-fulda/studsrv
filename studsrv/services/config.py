


class ConfigService(object):
  def __init__(self):
    pass
  
  
  def __getattr__(self, name):
    # TODO lookup in application configuration
    if name == 'users_volume':
      return '/mnt/users'
    
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
