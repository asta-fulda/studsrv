from django.db import models



class Image(models.Model):
  image_id = models.SlugField(primary_key = True,
                              default = None,
                              max_length = 256)
  
  title = models.CharField(default = None,
                           max_length = 256)

  description = models.TextField()


  def __unicode__(self):
      return self.image_id



# TODO: Add expires field
class Project(models.Model):
  name = models.SlugField(primary_key = True,
                          default = None,
                          max_length = 63)  # Length as specified by DNS name part

  image = models.ForeignKey(Image)

  description = models.TextField(blank = True)
  
  container_id = models.CharField(default = None,
                                  max_length = 64)

  created = models.DateTimeField(auto_now_add = True)
  
  enabled = models.BooleanField(default = True)

  blocked = models.TextField(null = True,
                             default = None)


  def __unicode__(self):
    return self.name
