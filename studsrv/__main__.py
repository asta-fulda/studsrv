from studsrv.frontend import app
from studsrv import db



@app.teardown_appcontext
def shutdown_session(exception = None):
    db.session.remove()



def main():
  app.run(host = 'localhost',
          port = 8000,
          debug = True)


if __name__ == '__main__':
  main()
