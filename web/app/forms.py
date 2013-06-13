from flask.ext.wtf import Form, TextField, SubmitField, Required, PasswordField
from flask_security.forms import RegisterForm

class ExtendedRegisterForm(RegisterForm):
    name = TextField('name', validators=[Required()])
