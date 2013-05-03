import os
CSRF_ENABLED=True
SECRET_KEY='falafel'
basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', None)
