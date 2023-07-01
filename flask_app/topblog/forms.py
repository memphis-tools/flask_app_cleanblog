from flask_ckeditor import CKEditorField
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, BooleanField
from wtforms.validators import DataRequired, URL, Length, Email
from wtforms.fields import EmailField
import random

from .settings import LOREM_PICSUM_URIS_RANDOM_RANGE


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


class PostAddForm(FlaskForm):
    # dummy development feature which allows a default random image link from https://picsum.photos
    dummy_picsum_id = random.randrange(1, LOREM_PICSUM_URIS_RANDOM_RANGE)
    dummy_picsum_url = f"https://picsum.photos/id/{dummy_picsum_id}/1900/1267"

    title = StringField(label="TITLE", validators=[DataRequired(), Length(min=5, max=65)])
    subtitle = StringField(label="SUBTITLE", validators=[DataRequired(), Length(min=5, max=150)])
    description = CKEditorField(label="DESCRIPTION", validators=[DataRequired(),])
    img_url = StringField(label="IMAGE", default=f"{dummy_picsum_url}", validators=[DataRequired(), URL(),])
    submit = SubmitField("PUBLISH POST")


class PostUpdateForm(FlaskForm):
    title = StringField(label="TITLE", validators=[DataRequired(), Length(min=5, max=65)])
    subtitle = StringField(label="SUBTITLE", validators=[DataRequired(), Length(min=5, max=150)])
    description = CKEditorField(label="DESCRIPTION", validators=[DataRequired(),])
    img_url = StringField(label="IMAGE", validators=[DataRequired(), URL(),])
    submit = SubmitField("PUBLISH POST")


class PostDeleteForm(FlaskForm):
    decision = BooleanField(default=True)
    submit = SubmitField("DELETE POST")


class CommentForm(FlaskForm):
    description = CKEditorField(label="DESCRIPTION", validators=[DataRequired(),])
    submit = SubmitField("PUBLISH COMMENT")
