import app
import json
from flask.ext.login import login_required
from flask import request, jsonify, render_template, url_for, redirect, flash

show_canvas = True

@app.flask_app.route('/user/<user_name_route>/<map_name_route>', methods=['GET'])
def user_mapping(user_name_route, map_name_route):
    u = app.models.kaizen_user.user_with_name_route(user_name_route)
    if not u:
        flash('No user with name %s, should have 404ed' % user_name_route)
        return app.views.index.go_to_index()

    m = app.models.mapping.mapping_with_userid_and_name_route(u.id, map_name_route)
    if not m:
        #lol, try seeing if it's the name too
        m = app.models.mapping.mapping_with_userid_and_name(u.id, map_name_route)

    if not m:
        return redirect(url_for('404'))
#         flash('No mapping with name %s, should have 404ed' % map_name_route)
#         return redirect(url_for('user_profile', user_name_route=user_name_route))

    if not m.has_notes():
        flash('This mapping has no notes')
        return redirect(url_for('user_profile', name_route=user_name_route))

    sites = view_sites(m)
    return render_template('user_mapping.html', mapping=m, sites=sites)

#display a saved version at /user/<uname>/<mname>
#display an edit version at /user/<uname>/edit/<mname>
#     # TODO - Visualization.
#     vis = app.models.mapping.visualize(m)
#     return render_template('user_mapping.html',
#                            show_canvas=json.dumps(show_canvas),
#                            mapping=json.dumps(vis))

@app.flask_app.route('/user/<uname>/edit/<mname>', methods=['GET'])
@login_required
def user_mapping_edit(uname, mname):
    if g.user.name != uname:
        return redirect(url_for('user_mapping', uname=uname, mname=mname))
    vis = app.models.mapping.test_visualize("test mapping")
    return render_template('user_mapping.html', mapping=json.dumps(vis), show_canvas=json.dumps(True))

@app.flask_app.route('/reindex_note', methods=['GET'])
@login_required
def reindex_note():
    a = request.args.get('loopId', 0, type=int)
    b = request.args.get('mapId', 0, type=int)
    c = request.args.get('targetIndex', 0, type=int)
    return jsonify(result=a + b + c)

@app.flask_app.route('/save_state', methods=['POST'])
@login_required
def save_state():
    v = app.models.visualization.visualization_with_id(int(request.form.get('vid')))
    if v:
        v.update_node_state(json.loads(request.form.get('notes')),
                            json.loads(request.form.get('sites')),
                            json.loads(request.form.get('root')),
                            json.loads(request.form.get('links')))
        return jsonify(result='success');
    else:
        return jsonify(result='fail')

@app.flask_app.route('/name_note')
@login_required
def name_note():
    note_id = request.args.get('noteId', 0, type=int)
    new_name = request.args.get('newName', None, type=str)
    #TODO(cinjon) do something with name here
    return jsonify(result=new_name)

@app.flask_app.route('/name_site')
@login_required
def name_site():
    site_id = request.args.get('siteId', 0, type=int)
    new_name = request.args.get('newName', None, type=str)
    #TODO(cinjon) do something with name here
    return jsonify(result=new_name)

def view_sites(mapping):
    return [{'name':app.utility.clean_ascii(s.short_title()), 'title':app.utility.clean_ascii(s.short_title()), 'notes':s.notes_in_chrono_order()} for s in mapping.get_all_sites()]
