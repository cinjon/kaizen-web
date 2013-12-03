from app import flask_app
from flask import g, render_template, redirect, url_for
from app.forms import ExtendedRegisterForm
from app.models import kaizen_user
from flask_security.forms import LoginForm

@flask_app.route('/index', endpoint='', methods=['GET'])
@flask_app.route('/', methods=['GET'])
def index():
    if g.user:
        return user_index()
    else:
        return enter_index()

def go_to_index():
    return redirect(url_for('index'))

def enter_index():
    register_user_form = ExtendedRegisterForm()
    login_user_form = LoginForm()
    return render_template('index.html',
                           register_user_form=register_user_form,
                           login_user_form=login_user_form,
                           title='Kaizen. continuous improvement.')


def user_index():
    return redirect(url_for('user_profile_owner'))

@flask_app.route('/google34d3fe92d155a2aa')
@flask_app.route('/google34d3fe92d155a2aa.html')
def google_extension_verify():
    return render_template('google34d3fe92d155a2aa.html')
