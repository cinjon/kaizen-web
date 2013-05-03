from app import flask_app, utility
from flask.ext.login import login_required
from flask import g, request

@flask_app.route('/user/<name>/bindings', methods=['GET'])
@login_required
def user_bindings(id):
    #show bindings and allow for change on main site
    pass

@flask_app.route('/xhr_bindings', methods=['POST'])
@login_required
def xhr_bindings():
    if request.is_xhr:
        binding = request.form['binding']
        mapping = request.form['mapping']
        if binding and mapping:
            g.user.set_binding(binding, mapping)
            return utility.xhr_201(True)
        return utility.xhr_201(False)
