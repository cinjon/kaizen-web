from app import flask_app, utility
from flask.ext.login import login_required
from flask import g, request

@flask_app.route('/user/<name>/notes', methods=['GET'])
@login_required
def user_notes(id):
    #show bindings and allow for change on main site
    pass

@flask_app.route('/xhr_notes', methods=['POST'])
@login_required
def xhr_notes():
    if request.is_xhr:
        g.user.add_note(data=request.form)
        return utility.xhr_201(True)
