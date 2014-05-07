from studsrv.services.config import configs
from studsrv.frontend import app



def main():
  app.run(host = configs.web_host,
          port = int(configs.web_port),
          debug = True)


if __name__ == '__main__':
  main()
