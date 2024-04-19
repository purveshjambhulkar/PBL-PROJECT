from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, EmailField, PasswordField
from wtforms.validators import DataRequired, length, Email

# WTForm for creating a blog post
# class CreatePostForm(FlaskForm):
#     title = StringField("Blog Post Title", validators=[DataRequired()])
#     subtitle = StringField("Subtitle", validators=[DataRequired()])
#     img_url = StringField("Blog Image URL", validators=[DataRequired(), URL()])
#     body = CKEditorField("Blog Content", validators=[DataRequired()])
#     submit = SubmitField("Submit Post")


# TODO: Create a RegisterForm to register new users
class CreateUserRegistrationForm(FlaskForm):
    email = EmailField("Email", validators=[DataRequired(), Email()])
    username = StringField("Username", validators=[DataRequired(), length(max=20)])
    password = PasswordField("Password ", validators=[DataRequired(), length(min=8, max=20)])
    sign_in = SubmitField("Register")


# TODO: Create a LoginForm to login existing users
class CreateLoginForm(FlaskForm):
    email = EmailField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired(), length(min=8, max=20)])
    login = SubmitField("Login")

class SummarizeText(FlaskForm):
    text_field = StringField("StringField", validators=[DataRequired()])
    send = SubmitField("Send")