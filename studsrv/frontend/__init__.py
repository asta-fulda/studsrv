import random
import string

from flask import Flask
from flask.ext import login

from studsrv.frontend import index
from studsrv.frontend import user

from studsrv.services.login import logins



app = Flask(__name__)

app.config['SECRET_KEY'] = ''.join(random.SystemRandom().choice(string.ascii_letters + string.digits) for _ in range(64))

logins.initApplication(app)

app.add_url_rule('/', view_func = index.IndexView.as_view('index'))

app.add_url_rule('/login', view_func = index.LoginView.as_view('login'))
app.add_url_rule('/logout', view_func = login.login_required(index.LogoutView.as_view('logout')))

app.add_url_rule('/user', view_func = login.login_required(user.IndexView.as_view('user.index')))
app.add_url_rule('/user/project', view_func = login.login_required(user.ProjectCreateView.as_view('user.project.create')))
app.add_url_rule('/user/project/<name>', view_func = login.login_required(user.ProjectDetailsView.as_view('user.project.details')))
app.add_url_rule('/user/project/<name>/start', view_func = login.login_required(user.ProjectStartView.as_view('user.project.start')))
app.add_url_rule('/user/project/<name>/stop', view_func = login.login_required(user.ProjectStopView.as_view('user.project.stop')))
app.add_url_rule('/user/project/<name>/delete', view_func = login.login_required(user.ProjectDeleteView.as_view('user.project.delete')))
app.add_url_rule('/user/project/<name>/admins/add', view_func = login.login_required(user.ProjectAddAdminView.as_view('user.project.admin.add')))
app.add_url_rule('/user/project/<name>/admins/remove', view_func = login.login_required(user.ProjectRemoveAdminView.as_view('user.project.admin.remove')))
