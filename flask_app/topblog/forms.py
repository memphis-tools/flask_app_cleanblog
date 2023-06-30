from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, URL, Length, Email
from wtforms.fields import EmailField


class ContactForm(FlaskForm):
    username = StringField(label="USERNAME", validators=[DataRequired(), Length(min=5, max=25)])
    email = EmailField("EMAIL", validators=[Email(),])
    message = TextAreaField("MESSAGE", validators=[DataRequired(),])
    submit = SubmitField("SEND MAIL")


class LoginForm(FlaskForm):
    username = StringField(label="USERNAME", validators=[DataRequired(), Length(min=5, max=25)])
    email = EmailField(label="EMAIL", validators=[DataRequired(),])
    password = PasswordField(label="PASSWORD", validators=[DataRequired(),])
    submit = SubmitField("LOG IN")


class SigninForm(FlaskForm):
    username = StringField(label="USERNAME", validators=[DataRequired(), Length(min=5, max=25)])
    email = EmailField(label="EMAIL", validators=[DataRequired(), Email()])
    password = PasswordField(label="PASSWORD", validators=[DataRequired(),])
    submit = SubmitField("SIGN IN")


class UserForm(FlaskForm):
    email = EmailField(label="EMAIL", validators=[Email(),])
    password = PasswordField(label="PASSWORD", validators=[Length(min=5, max=25),])
    website = StringField(label="PERSONAL WEBSITE", validators=[URL(),])
    submit = SubmitField("UPDATE")
