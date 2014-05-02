import configparser



class Image(object):
  def __init__(self,
               name,
               title):
    self.__name = name
    self.__title = title
    
    
  @property
  def name(self):
    return self.__name
  
  
  @property
  def title(self):
    return self.__title



class ImageService(object):
  PATH = '/etc/studsrv/images.ini'
  
  
  def __init__(self):
    parser = configparser.SafeConfigParser()
    parser.read('/etc/studsrv/images.ini')
    
    self.__images = {name: Image(name = name,
                                 title = section['title'])
                     for name, section
                     in ((name, parser[name])
                         for name
                         in parser.sections())}

  
  def getImages(self):
    return self.__images.keys()
    
    
  def getImage(self,
               name):
    return self.__images[name]


images = ImageService()
