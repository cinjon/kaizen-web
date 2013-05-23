from flask import request, g
from flask.ext.login import current_user
from app.models import kaizen_user
from app.views.index import go_to_index
from app import flask_app, lm
from app import utility

@lm.user_loader
def load_user(id):
    return kaizen_user.user_with_id(id)

@flask_app.before_request
def before_request():
    if current_user.is_anonymous():
        g.user = None
    else:
        g.user = current_user

def handle_g_user():
    if request.is_xhr:
        return utility.xhr_user_login(g.user, True)
    return go_to_index()

