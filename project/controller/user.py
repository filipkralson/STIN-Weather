from flask import Blueprint, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, EqualTo
from project.object.users import db as users_db, User, getUser
from project.utils.cookies import createCookie, readCookie, deleteCookie

user = Blueprint('user', __name__)


class Login(FlaskForm):
    user = StringField("Username", validators=[InputRequired()], render_kw=dict(class_="form-control"))
    password = PasswordField("Password", validators=[InputRequired()], render_kw=dict(class_="form-control"))
    submit = SubmitField("Sign in", render_kw=dict(class_="btn btn-outline-primary btn-block"))


class Register(FlaskForm):
    user = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])
    card = StringField("Card number", validators=[InputRequired()])
    confirm_password = PasswordField("Password again", validators=[InputRequired(), EqualTo('password',
                                                                                            message='Not matching!')])
    submit = SubmitField("Sign Up")


def currentUser():
    cookie = readCookie()
    if cookie:
        username = cookie["username"]
        if username and getUser(username):
            return getUser(username)
        else:
            return None
    return None


@user.route('/register', methods=['GET', 'POST'])
def signUp():
    form = Register()
    error = None

    if form.validate_on_submit():
        if not getUser(form.user.data):
            new_user = User(name=form.user.data, password=form.password.data, card_number=form.card.data)
            try:
                users_db.session.add(new_user)
                users_db.session.commit()
            except Exception as e:
                print(e)
                users_db.session.rollback()
                error = "Cannot register!"
                return render_template("register.html", form=form, error=error)
            return createCookie(form.user.data)
        else:
            error = 'User already exists!'

    return render_template("register.html", form=form, error=error)


@user.route('/login', methods=['GET', 'POST'])
def signIn():
    form = Login()
    error = None

    if form.validate_on_submit():
        user_from = getUser(form.user.data)
        if user_from and user_from.checkPasswd(form.password.data):
            return createCookie(user_from.name)
        else:
            error = 'Wrong username or password!'

    return render_template("login.html", form=form, error=error)


@user.route('/logout')
def exit():
    return deleteCookie()
