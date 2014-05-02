


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
  def getImages(self):
    return [Image(name = 'static',
                  title = 'Statische Webseite')]


images = ImageService()
