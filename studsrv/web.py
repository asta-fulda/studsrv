from studsrv.frontend import app



def main():
  app.run(host = 'localhost',
          port = 8000,
          debug = True)


if __name__ == '__main__':
  main()
