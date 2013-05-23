import os
CSRF_ENABLED = True
SECRET_KEY = 'falafel'
basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', os.environ.get('KAIZEN_DATABASE_URL', None))

MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 465
MAIL_USE_TLS = False
MAIL_USE_SSL = True
MAIL_USERNAME = 'chimu.kaizen@gmail.com'
MAIL_PASSWORD = 'abkaizen'
MAIL_DEFAULT_SENDER = 'chimu.kaizen@gmail.com'
MAIL_SUPPRESS_SEND = False

# Flask-Security Flags
SECURITY_CONFIRMABLE = True
SECURITY_REGISTERABLE = True
SECURITY_RECOVERABLE = True
SECURITY_TRACKABLE = True

ADMINS = ['chimu.kaizen@gmail.com']