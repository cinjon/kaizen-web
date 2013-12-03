import os
CSRF_ENABLED = True
SECRET_KEY = 'falafel'
basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', os.environ.get('KAIZEN_DATABASE_URL', None))

MAIL_SERVER = os.environ.get('KAIZEN_MAIL_SERVER')
MAIL_PORT = os.environ.get('KAIZEN_MAIL_PORT')
MAIL_USE_TLS = os.environ.get('KAIZEN_MAIL_USE_TLS')
MAIL_USE_SSL = os.environ.get('KAIZEN_MAIL_USE_SSL')
MAIL_USERNAME = os.environ.get('KAIZEN_MAIL_USERNAME')
MAIL_PASSWORD = os.environ.get('KAIZEN_MAIL_PASSWORD')
MAIL_DEFAULT_SENDER = os.environ.get('KAIZEN_MAIL_DEFAULT_SENDER')
MAIL_SUPPRESS_SEND = os.environ.get('KAIZEN_MAIL_SUPPRESS_SEND')

# Flask-Security Flags
SECURITY_CONFIRMABLE = False
SECURITY_REGISTERABLE = True
SECURITY_RECOVERABLE = True
SECURITY_TRACKABLE = True
SECURITY_PASSWORD_HASH = 'sha512_crypt'
SECURITY_PASSWORD_SALT = '!#*PFK%WOq3j3kf'

ADMINS = ['chimu.kaizen@gmail.com']
