from app import flask_app
from flask import g, render_template, flash, redirect, url_for
from flask.ext.login import login_required
from app.forms import RegisterForm, LoginForm
from app.models import user

@flask_app.route('/index', endpoint='', methods=['GET', 'POST'])
@flask_app.route('/', methods=['GET', 'POST'])
def index():
    if g.user:
        return user_index()
    else:
        return enter_index()

def go_to_index():
    return redirect(url_for('index'))

def enter_index():
    register_form = RegisterForm()
    login_form = LoginForm()
    if register_form.validate_on_submit():
        return user.try_register(register_form.email.data, register_form.password.data,
                                 register_form.first.data, register_form.last.data,
                                 xhr=False)
    if login_form.validate_on_submit():
        return user.try_login(login_form.email.data, login_form.password.data,
                              login_form.remember_me.data, xhr=False)
    return render_template('index.html', register_form=register_form, login_form=login_form, title='Kaizen. continuous improvement.')

def user_index():
    #TODO
    #This is going to show my maps on a sidebar as well as everyone's maps
    #or friend's maps or some such on the main area
    users = []
    for u in user.all_users_sorted_by_note_total():
        if u.email == g.user.email:
            continue
        users.append({'first':u.first, 'last':u.last,
                      'map_total':len(u.mappings.all()),
                      'note_total':u.number_of_notes()})
    mappings = []
    for m in g.user.get_all_mappings_in_name_order():
        mappings.append({'name':str(m.name), 'sites':len(m.get_all_sites()),
                         'notes':len(m.get_all_notes())})
    return render_template('global_index.html', users=users, mappings=mappings)

@flask_app.route('/google34d3fe92d155a2aa')
@flask_app.route('/google34d3fe92d155a2aa.html')
def google_extension_verify():
    return render_template('google34d3fe92d155a2aa.html')
