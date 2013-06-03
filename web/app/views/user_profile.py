from app import flask_app
from app.models import kaizen_user, mapping
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

# def format_datetime(value, format='medium'):
#     if format == 'full':
#         format="EEEE, d. MMMM y 'at' HH:mm"
#     elif format == 'medium':
#         format="EE dd.MM.y HH:mm"
#     return babel.format_datetime(value, format)
#
# flask_app.jinja_env.filters['datetimeformat'] = format_datetime


def view_mappings(u):
    mappings = []
    # for m in u.get_current_mappings(mapping.Mapping.creation_time):
    for m in u.get_all_mappings_in_name_order():
        if m.binding > -1:
            mappings.append({'name':str(m.name), 'binding':m.binding, 'notes':m.get_all_notes()})
        else:
            mappings.append({'name':str(m.name), 'binding':'-', 'notes':m.get_all_notes()})
    return mappings


