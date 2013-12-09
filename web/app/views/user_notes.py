import app
from flask.ext.login import login_required
from flask import g, request, jsonify, redirect, url_for

@app.flask_app.route('/user/<name>/notes', methods=['GET'])
@login_required
def user_notes(id):
    #show bindings and allow for change on main site
    pass

@app.flask_app.route('/xhr_notes', methods=['POST'])
@login_required
def xhr_notes():
    if request.is_xhr:
        g.user.add_note(data=request.form)
        return app.utility.xhr_201(True)

@app.flask_app.route('/delete_note', methods=['GET', 'POST'])
@login_required
def delete_note():
    noteId = request.args.get('noteId', 0, type=int)
    note = app.models.note.note_with_id(noteId)
    if not note:
        return jsonify(success=False)

    note.delete()
    map_has_sites = True
    site_num_notes = note.site.num_notes()
    if site_num_notes == 0:
        map_has_sites = note.mapping.has_notes()
    return jsonify(success=True, noteId=noteId,
                   siteNumNotes=site_num_notes,
                   mapHasSites=map_has_sites)
