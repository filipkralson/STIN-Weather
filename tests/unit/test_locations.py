import pytest
from utils.database import db
from flask import Flask
from object.locations import Location
from object.users import User

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

def test_location_creation(init_db):
    # Vytvoření uživatele pro test
    user = User(name='test_user', password="password", card_number="1234567890123456")
    db.session.add(user)
    db.session.commit()

    # Vytvoření umístění
    location = Location(location='Test Location', user=user)

    # Test, zda je umístění vytvořeno správně
    assert location.id is not None
    assert location.location == 'Test Location'
    assert location.user == user

def test_location_deletion(init_db):
    # Vytvoření uživatele a umístění pro test
    user = User(name='test_user', password="password", card_number="1234567890123456")
    location = Location(location='Test Location', user=user)
    db.session.add(user)
    db.session.add(location)
    db.session.commit()

    # Smazání umístění
    location.delete_location()

    # Test, zda bylo umístění úspěšně smazáno
    assert db.session.get(Location, location.id) is None

