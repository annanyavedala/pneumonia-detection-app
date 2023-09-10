from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField,IntegerField
from wtforms.fields.core import IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from flask_wtf.file import FileField, FileAllowed


class RegistrationForm(FlaskForm):
    username = StringField('Username',  validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    phone_number=IntegerField('Phone number',validators=[DataRequired()])
    Age=IntegerField('Age',validators=[DataRequired()])
    Height=IntegerField('Height',validators=[DataRequired()])
    Weight=IntegerField('Weight',validators=[DataRequired()])
  
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class UploadImage(FlaskForm):
    picture=FileField('Upload your lung xray image here', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    submit = SubmitField('Get results!')

class Permission(FlaskForm):
    share=BooleanField('permission to share')
    submit=SubmitField('share')