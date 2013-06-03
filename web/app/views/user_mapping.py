from app import models, flask_app
from app.views.index import go_to_index
import json
from flask.ext.login import login_required
from flask import request, jsonify, render_template, url_for, redirect, flash

show_canvas = True

#display a saved version at /user/<uname>/<mname>
#display an edit version at /user/<uname>/edit/<mname>


# @flask_app.route('/user/<uname>/<mname>', methods=['GET'])
# def user_mapping(uname, mname):
#     u = models.kaizen_user.user_with_name(uname)
#     if not u:
#         flash('No user with name %s, should have 404ed' % uname)
#         return go_to_index()
#
#     m = models.mapping.mapping_with_userid_and_name(u.id, mname)
#     if not m:
#         flash('No mapping with name %s, should have 404ed' % mname)
#         return redirect(url_for('user_profile', name=uname))
#
#     vis = models.mapping.visualize(m)
#     return render_template('user_mapping.html', user=u, mapping=json.dumps(vis), mname=json.dumps(m.name), show_canvas=json.dumps(show_canvas))

@flask_app.route('/remove_index', methods=['GET'])
@login_required
def remove_index():
    a = request.args.get('loopId', 0, type=int)
    b = request.args.get('mapId', 0, type=int)
    return jsonify(result=a + b)

@flask_app.route('/reindex_note', methods=['GET'])
@login_required
def reindex_note():
    a = request.args.get('loopId', 0, type=int)
    b = request.args.get('mapId', 0, type=int)
    c = request.args.get('targetIndex', 0, type=int)
    return jsonify(result=a + b + c)


@flask_app.route('/user/<uname>/<mname>', methods=['GET'])
def user_mapping(uname, mname):
    u = models.kaizen_user.user_with_name(uname)
    if not u:
        flash('No user with name %s, should have 404ed' % uname)
        return go_to_index()

    m = models.mapping.mapping_with_userid_and_name(u.id, mname)
    if not m:
        flash('No mapping with name %s, should have 404ed' % mname)
        return redirect(url_for('user_profile', name=uname))

    vis = models.mapping.visualize(m)
<<<<<<< HEAD
    return render_template('user_mapping.html', user=u,
                           show_canvas=json.dumps(show_canvas), mapping=json.dumps(vis))
=======
    return render_template('user_mapping.html', user=u, mapping=m, mname=m.name, show_canvas=json.dumps(show_canvas))
    # return render_template('user_paper_mapping.html', user=u, mapping=m, mname=m.name, show_canvas=json.dumps(show_canvas))
>>>>>>> da94811... some front end work



@flask_app.route('/user/<uname>/edit/<mname>', methods=['GET'])
# @login_required
def user_mapping_edit(uname, mname):
#     if g.user.name != uname:
#         return redirect(url_for('user_mapping', uname=uname, mname=mname))
    vis = models.mapping.test_visualize("test mapping")
    return render_template('user_mapping.html', mapping=json.dumps(vis), show_canvas=json.dumps(True))


