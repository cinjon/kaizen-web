#!venv/bin/python
from app import db
from app import flask_app
db.create_all()
flask_app.run(debug=True)
