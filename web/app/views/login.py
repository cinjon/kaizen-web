from flask import request, g
from flask.ext.login import logout_user, current_user, login_required
from app.models import user
from app.views.index import go_to_index
from app import flask_app, lm
from app import utility

@lm.user_loader
def load_user(id):
    return user.user_with_id(id)

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

@flask_app.route('/login', methods=['GET', 'POST'])
def login():
    #only for the extension
    if g.user:
        return handle_g_user()
    if request.is_xhr:
        email = request.form['email']
        password = request.form['password']
        return user.try_login(email, password, xhr=True)
    return go_to_index()

@flask_app.route('/logout')
@login_required
def logout():
    logout_user()
    if request.is_xhr:
        return utility.xhr_response({}, 200)
    return go_to_index()

