import datetime
from flask import Flask, abort, render_template, redirect, url_for, flash, request
from flask_bootstrap import Bootstrap5
from flask_ckeditor import CKEditor
from flask_login import UserMixin, login_user, LoginManager, current_user, logout_user
from flask_sqlalchemy import SQLAlchemy
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
from markupsafe import Markup
from datetime import date
import smtplib
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField
from wtforms.validators import DataRequired, URL
from flask_ckeditor import CKEditorField
from sqlalchemy.orm import relationship, registry
import os

# Import your forms from the forms.py
from forms import CreateUserRegistrationForm, CreateLoginForm, SummarizeText
from transformers import pipeline


app = Flask(__name__)
# MY_EMAIL = os.environ.get("EMAIL")
# MY_PASSWORD = os.environ.get("EMAIL_PASSWORD")

app.config['SECRET_KEY'] = "mySecretKey"
Bootstrap5(app)
CKEditor(app)

# CONNECT TO DB
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///users.db"
db = SQLAlchemy()
db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)

summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

@login_manager.user_loader
def load_user(user_id):
    return db.get_or_404(User, user_id)


class User(UserMixin, db.Model):
    __tablename__ = "user_data"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(500), nullable=False)
    username = db.Column(db.String(100), unique=True, nullable=False)


with app.app_context():
    db.create_all()


def admin_only(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.id != 1:
            return abort(403)
        return f(*args, **kwargs)
    return decorated_function


@app.route("/")
def home():
    return render_template("home.html")


@app.route('/register', methods=["GET", "POST"])
def register():
    form = CreateUserRegistrationForm()
    if form.validate_on_submit():
        email = form.email.data
        username = form.username.data
        password = generate_password_hash(password=form.password.data, method='pbkdf2:sha256', salt_length=8)
        fetch_email = db.session.execute(db.select(User).where(User.email == email)).scalar()
        if fetch_email:
            flash("This email is already registered with the blog website try to login")
            return redirect(url_for("login"))
        fetch_username = db.session.execute(db.select(User).where(User.username == username)).scalar()
        if fetch_username:
            form.username.errors.append("This username is not available")
            form.username.errors.reverse()
            return render_template("register.html", form=form)
        new_user = User(email=email, password=password, username=username)
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return redirect(url_for("home"))
    return render_template("register.html", form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = CreateLoginForm()
    if form.validate_on_submit():
        user = db.session.execute(db.select(User).where(User.email == form.email.data)).scalar()
        if not user:
            form.email.errors.append("Invalid email address, If you don't have a account first Register.")
            form.email.errors.reverse()
        else:
            is_password_correct = check_password_hash(user.password, form.password.data)
            if not is_password_correct:
                form.password.errors.append("wrong Password")
                form.password.errors.reverse()
            else:
                login_user(user)
                return redirect(url_for("home"))
    return render_template("login.html", form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/summarize', methods=['GET', 'POST'])
def summarize():
    if current_user.is_authenticated:
        form = SummarizeText()
        if request.method == "POST":
            text = request.form.get("prompt")
            print(text)
            summary = summarizer(text, max_length=300, min_length=30, do_sample=False)[0]["summary_text"]
            print(summary)
            flash(summary, "success")
            return redirect(url_for('summarize'))
        return render_template("chat.html", form=form)
    else:
        # flash("In order to view the post you have to login first")
        return redirect(url_for("login"))


@app.route("/team-profiles")
def profiles():
    return render_template("team-profiles.html")


app.run(debug=True)