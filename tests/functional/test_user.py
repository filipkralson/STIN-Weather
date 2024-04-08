import pytest
from flask import Flask, url_for
from utils.database import db
from object.users import User
from controller.user import user


@pytest.fixture
def app():
    app = Flask(__name__, template_folder='../templates')
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.register_blueprint(user)
    db.init_app(app)
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


def test_signup_route(client):
    pass


def test_signup_success(client, mocker):
    pass


def test_signup_failure_existing_user(client, mocker):
    pass


def test_login_route(client):
    pass


def test_login_success(client, mocker):
    pass


def test_login_failure(client, mocker):
    pass


def test_logout_route(client):
    pass
