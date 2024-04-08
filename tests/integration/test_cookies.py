import pytest
from flask import Flask
from utils.database import db
from utils.cookies import readCookie, createCookie, deleteCookie, get_current_user


@pytest.fixture
def app():
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    return app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def init_db(app):
    db.init_app(app)
    with app.app_context():
        db.create_all()
        yield db
        db.session.remove()
        db.drop_all()


def test_readCookie(client):
    pass


def test_createCookie(client):
    pass


def test_deleteCookie(client):
    pass


def test_get_current_user_with_mock(app, monkeypatch, init_db):
    pass
