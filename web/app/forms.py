from flask.ext.wtf import Form, TextField, BooleanField, Required, PasswordField

class LoginForm(Form):
    email = TextField('email', validators=[Required()])
    password = PasswordField('password', validators=[Required()])
    remember_me = BooleanField('remember_me', default=False)

class RegisterForm(Form):
    email = TextField('email', validators=[Required()])
    password = PasswordField('password', validators=[Required()])
    first = TextField('first', validators=[Required()])
    last = TextField('first', validators=[Required()])
