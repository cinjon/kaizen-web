from app import flask_app
from app.models import kaizen_user
from flask import g, render_template, redirect, flash, url_for
from flask.ext.login import login_required

@flask_app.route('/me')
@login_required
def user_profile_owner():
    return render_template('user_profile.html', user=g.user, mappings=view_mappings(g.user))

@flask_app.route('/user/<name>')
@login_required
def user_profile(name):
    if g.user and g.user.name == name:
        return render_template('user_profile.html', user=g.user, mappings=view_mappings(g.user))

    viewed = kaizen_user.user_with_name(name)
    if viewed:
        return render_template('user_profile.html', user=viewed, mappings=view_mappings(viewed))
    flash('No user with name %s, should have 404ed' % name)
    #TODO return no user with name 404 page

def view_mappings(u):
    mappings = []
    for m in u.get_all_mappings_in_name_order():
        if m.binding > -1:
            mappings.append({'name':str(m.name), 'binding':m.binding, 'notes':len(m.get_all_notes())})
        else:
            mappings.append({'name':str(m.name), 'binding':'-', 'notes':len(m.get_all_notes())})
    return mappings


