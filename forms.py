from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, PasswordField
from wtforms.validators import DataRequired, EqualTo, Length


class Login(FlaskForm):
    account = StringField(u'account', validators=[DataRequired()])
    password = PasswordField(u'password', validators=[DataRequired()])
    submit = SubmitField(u'login')

class RegisterForm(FlaskForm):
    user_name = StringField(u'user_name', validators=[DataRequired()])
    account = StringField(u'account', validators=[DataRequired()])
    password = PasswordField(u'password', validators=[DataRequired()])
    repeat_password = PasswordField(u'repeat_password', validators=[DataRequired()])
    submit = SubmitField(u'sign up')

class SearchBookForm(FlaskForm):
    methods = [('book_name', 'book name'), ('author', 'author'), ('isbn', 'ISBN'), ('intr', 'introduction')]
    method = SelectField(choices=methods, validators=[DataRequired()], coerce=str)
    content = StringField(validators=[DataRequired()])
    submit = SubmitField('Search')

class SearchUserForm(FlaskForm):
    methods = [('username', 'user name'), ('account_name', 'account id'), ('type', 'user type')]
    method = SelectField(choices=methods, validators=[DataRequired()], coerce=str)
    content = StringField(validators=[DataRequired()])
    submit = SubmitField('Search')

class SearchCommentForm(FlaskForm):
    methods = [('book_name', 'book name'), ('user_name', 'user name'), ('content', 'comment'), ('time', 'time')]
    method = SelectField(choices=methods, validators=[DataRequired()], coerce=str)
    content = StringField(validators=[DataRequired()])
    submit = SubmitField('Search')

class ChangePasswordForm(FlaskForm):
    old_password = PasswordField(u'Original password', validators=[DataRequired()])
    password = PasswordField(u'New password', validators=[DataRequired(), EqualTo('password2', message=u'The two passwords must be same')])
    password2 = PasswordField(u'Confirm new password', validators=[DataRequired()])
    submit = SubmitField(u'Confirm')