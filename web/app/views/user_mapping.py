import json
from app import flask_app, utility
from app.models import user, mapping
from app.views.index import go_to_index
from flask import g, render_template, url_for, redirect
from flask.ext.login import login_required

show_canvas = True

#display a saved version at /user/<uname>/<mname>
#display an edit version at /user/<uname>/edit/<mname>

@flask_app.route('/user/<uname>/<mname>', methods=['GET'])
def user_mapping(uname, mname):
    u = user.user_with_name(uname)
    if not u:
        flash('No user with name %s, should have 404ed' % uname)
        return go_to_index()

    m = mapping.mapping_with_userid_and_name(u.id, mname)
    if not m:
        flash('No mapping with name %s, should have 404ed' % mname)
        return redirect(url_for('user_profile', name=uname))

    vis = mapping.visualize(m)
    return render_template('user_mapping.html', user=u, mapping=json.dumps(vis), mname=json.dumps(m.name), show_canvas=json.dumps(show_canvas))

@flask_app.route('/user/<uname>/edit/<mname>', methods=['GET'])
# @login_required
def user_mapping_edit(uname, mname):
#     if g.user.name != uname:
#         return redirect(url_for('user_mapping', uname=uname, mname=mname))
    vis = mapping.test_visualize("test mapping")
    return render_template('user_mapping.html', mapping=json.dumps(vis), show_canvas=json.dumps(True))


