from flask.ext.wtf import Form, TextField, SubmitField, Required, PasswordField
from flask_security.forms import RegisterForm

class ExtendedRegisterForm(RegisterForm):
    first = TextField('first', validators=[Required()])
    last = TextField('last', validators=[Required()])
