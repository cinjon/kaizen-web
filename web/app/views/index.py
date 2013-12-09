import app
from flask import g, render_template, redirect, url_for
from app.models import kaizen_user
from flask_security.forms import LoginForm
from app.forms import ExtendedRegisterForm

@app.flask_app.route('/', methods=['GET', 'POST'])
def index():
    if g.user:
        return user_index()
    else:
        return enter_index()

def enter_index():
    return render_template('index.html',
                           register_user_form=ExtendedRegisterForm(),
                           login_user_form=LoginForm())

def user_index():
    return redirect('/me')

def go_to_index():
    return redirect(url_for('index'))

@app.flask_app.route('/google34d3fe92d155a2aa')
@app.flask_app.route('/google34d3fe92d155a2aa.html')
def google_extension_verify():
    return render_template('google34d3fe92d155a2aa.html')

@app.flask_app.route('/features')
def new_features():
    return render_template('new_features.html')
