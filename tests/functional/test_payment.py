import pytest
from flask import Flask, url_for
from utils.database import db
from object.users import User


@pytest.fixture
def app():
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


def test_payment_route_redirects_to_signin_when_not_logged_in():
    pass


def test_payment_route_redirects_to_signup_when_user_not_found():
    pass


def test_payment_route_sets_user_subscription_when_logged_in():
    pass
