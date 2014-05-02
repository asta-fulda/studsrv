import docker



def get_connection():
  return docker.Client()
