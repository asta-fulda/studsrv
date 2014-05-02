


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
  images = {'static': Image('static', 'Statische Webseite')}
  
  def getImages(self):
    return self.images.keys()
    
    
  def getImage(self,
               name):
    return self.images[name]


images = ImageService()
