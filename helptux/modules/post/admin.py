from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectMultipleField
from wtforms.validators import Required, Email, EqualTo


class PostCreateForm(Form):
    pass


class PostEditForm(Form):
    pass


class PostDeleteForm(Form):
    pass
