from app import flask_app
from flask import redirect, url_for, request
from app.models import user

@flask_app.route('/register', methods=['GET', 'POST'])
def register():
    #only for the extension
    if request.is_xhr:
        email = request.form['email']
        password = request.form['password']
        first = request.form['first']
        last = request.form['last']
        return user.try_register(email, password, first, last, xhr=True)
    return redirect(url_for('index'))
