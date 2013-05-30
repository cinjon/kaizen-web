from flask import Flask
from forms import ExtendedRegisterForm
from flask.ext.mail import Mail
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from flask.ext.security import Security, SQLAlchemyUserDatastore
import utility

flask_app = Flask(__name__)
flask_app.config.from_object('config')
flask_app.debug = True
db = SQLAlchemy(flask_app)

lm = LoginManager()
lm.setup_app(flask_app)
lm.login_view = 'login'

mail = Mail(flask_app)

@flask_app.before_first_request
def before_first_request():
    try:
        db.create_all()
    except Exception, e:
        flask_app.logger.error(str(e))

import models
security_ds = SQLAlchemyUserDatastore(db, models.kaizen_user.KaizenUser, models.role.Role)
security = Security(flask_app,
                    security_ds,
                    register_form=ExtendedRegisterForm,
                    confirm_register_form=ExtendedRegisterForm)
flask_app.security = security

import views
