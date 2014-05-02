import configparser



class ConfigService(object):
  def __init__(self):
    parser = configparser.RawConfigParser()
    parser.read('/etc/studsrv/config.ini')
    
    self.__configs = {}
    
    for section in parser.sections():
      for key in parser[section]:
        self.__configs['%s_%s' % (section, key)] = parser[section][key] 
    
  
  def __getattr__(self, name):
    return self.__configs[name]


configs = ConfigService()
