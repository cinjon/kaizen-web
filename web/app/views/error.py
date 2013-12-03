from app import flask_app
from flask import render_template

@flask_app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
