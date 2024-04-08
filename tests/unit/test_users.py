import pytest
from flask import Flask
from object.users import User, db


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


def test_create_user():
    user = User(name='test_user', password='password123', card_number='1234567890123456')

    assert user.name == 'test_user'
    assert user.checkPasswd('password123')
    assert user.card_number == '1234567890123456'


def test_add_town(app):
    user = User(name='test_user', password='password123', card_number='1234567890123456')
    db.session.add(user)
    db.session.commit()

    user.add('New York')

    town_count = user.towns.count()

    assert town_count == 1


def test_get_user(app):
    user = User(name='test_user', password='password123', card_number='1234567890123456')
    db.session.add(user)
    db.session.commit()

    retrieved_user = User.query.filter_by(name='test_user').first()

    assert retrieved_user is not None
    assert retrieved_user.name == 'test_user'
