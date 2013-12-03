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
SECURITY_POST_REGISTER_VIEW = 'me'
SECURITY_POST_LOGIN_VIEW = 'me'
SECURITY_RECOVERABLE = True
SECURITY_TRACKABLE = True
SECURITY_PASSWORD_HASH = 'sha512_crypt'
SECURITY_PASSWORD_SALT = '!#*PFK%WOq3j3kf'
SECURITY_MSG_USER_DOES_NOT_EXIST = ('That email is not these parts', 'error')
SECURITY_MSG_INVALID_PASSWORD = ('That password was not right', 'error')
SECURITY_MSG_PASSWORD_NOT_PROVIDED = ('Password por favor', 'error')
SECURITY_MSG_EMAIL_NOT_PROVIDED = ('Email por favor', 'error')

ADMINS = ['chimu.kaizen@gmail.com']
