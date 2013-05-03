import os
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager

flask_app = Flask(__name__)
flask_app.config.from_object('config')
flask_app.debug = True
db = SQLAlchemy(flask_app)

lm = LoginManager()
lm.setup_app(flask_app)
lm.login_view = 'login'

import utility
import models
import views
