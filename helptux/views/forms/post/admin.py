from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectMultipleField, SelectField,\
    TextAreaField, HiddenField
from wtforms.validators import Required, Email, EqualTo


class AngularJSHiddenField(HiddenField):
    def __call__(self, **kwargs):
        for key in list(kwargs):
            if key.startswith('ng_'):
                kwargs['ng-' + key[3:]] = kwargs.pop(key)
        return super(AngularJSHiddenField, self).__call__(**kwargs)

class PostCreateForm(Form):
    title = StringField('Title', validators=[Required()])
    content = TextAreaField('Content', validators=[Required()])
    type = SelectField('Type', validators=[Required()], coerce=int)
    tags = AngularJSHiddenField('Tag', validators=[])
    submit = SubmitField('Save')


class PostEditForm(Form):
    pass


class PostDeleteForm(Form):
    pass
