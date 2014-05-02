from flask import Flask
from flask.ext import login

from studsrv.frontend import index
from studsrv.frontend import user

from studsrv.services.user import users



app = Flask(__name__)

app.config['SECRET_KEY'] = '123456790'


login_manager = login.LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(username):
  return users.getUser(username)


app.add_url_rule('/', view_func = index.IndexView.as_view('index'))

app.add_url_rule('/login', view_func = index.LoginView.as_view('login'))
app.add_url_rule('/logout', view_func = index.LogoutView.as_view('logout'))

app.add_url_rule('/user', view_func = user.IndexView.as_view('user.index'))
app.add_url_rule('/user/project', view_func = user.ProjectCreateView.as_view('user.project.create'))
app.add_url_rule('/user/project/<name>', view_func = user.ProjectDetailsView.as_view('user.project.details'))
app.add_url_rule('/user/project/<name>/start', view_func = user.ProjectStartView.as_view('user.project.start'))
app.add_url_rule('/user/project/<name>/stop', view_func = user.ProjectStopView.as_view('user.project.stop'))
