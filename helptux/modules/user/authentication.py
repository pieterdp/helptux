from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import Required, Email


class LoginForm(Form):
    email = StringField('E-mail', validators=[Required(), Email()])
    password = PasswordField('Password', validators=[Required()])
    remember_me = BooleanField('Onthouden')
    submit = SubmitField('Aanmelden')
