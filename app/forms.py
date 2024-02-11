from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, SelectField, DateField
from wtforms.validators import DataRequired, Email, EqualTo, Length
from datetime import datetime

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

class ArticleForm(FlaskForm):
    title = StringField('Titre', validators=[DataRequired()])
    theme = SelectField('Thème', choices=[('race', 'Race'), ('nourriture', 'Nourriture'), ('jeux', 'Jeux')], validators=[DataRequired()])
    body = TextAreaField('Contenu', validators=[DataRequired()])
    timestamp = DateField('Date', format='%Y-%m-%d', default=datetime.now())
    author_id = StringField('Auteur', validators=[DataRequired()])
    submit = SubmitField('Validate')