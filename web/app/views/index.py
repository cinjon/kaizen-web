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
    #TODO
    #This is going to show my maps on a sidebar as well as everyone's maps
    #or friend's maps or some such on the main area
    users = []
    for u in kaizen_user.all_users_sorted_by_note_total():
        if u.email == g.user.email:
            continue
        users.append({'name':u.name,
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
