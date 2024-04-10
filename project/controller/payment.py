from flask import Blueprint, render_template, redirect, url_for, flash
from flask_wtf import FlaskForm
from wtforms.fields.simple import SubmitField
from project.utils.cookies import readCookie
from project.object.users import User

payment_bp = Blueprint('payment', __name__)


class PayForm(FlaskForm):
    submit = SubmitField("Pay", render_kw=dict(class_="btn btn-primary"))


@payment_bp.route('/payment', methods=['GET', 'POST'])
def payment():
    form = PayForm()
    if form.validate_on_submit():
        user_cookie = readCookie()
        if not user_cookie:
            flash('You need to be logged in to access the payment gateway.', 'error')
            return redirect(url_for('user.signIn'))

        username = user_cookie.get('username')
        user = User.query.filter_by(name=username).first()

        if user:
            user.setIsSubscribed(True)
            return redirect(url_for('main.get'))
        else:
            flash('User not found.', 'error')
            return redirect(url_for('user.signUp'))

    return render_template('pay.html', form=form)
