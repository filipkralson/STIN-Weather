import pytest
from project.object.users import User
from project.object.locations import Location
from app import create_app
from project.utils.database import db
import os


@pytest.fixture
def app():
    os.environ['CONFIG_TYPE'] = 'config.TestingConfig'
    app = create_app()
    return app


@pytest.fixture(scope='module')
def new_user():
    user = User('testUser', 'Password', card_number="123456789123456")
    return user


@pytest.fixture(scope='module')
def new_location():
    user = User('testUser', 'Password', card_number="123456789123456")
    new_location = Location('Praha', user)
    return new_location


@pytest.fixture(scope='module')
def test_client():
    os.environ['CONFIG_TYPE'] = 'config.TestingConfig'
    app = create_app()

    with app.test_client() as testing_client:
        with app.app_context():
            yield testing_client


@pytest.fixture(scope='module')
def init_database(test_client):
    db.create_all()

    default_user = User("testUser", "password", card_number="123456789123456")
    second_user = User("testUser1", "password1", card_number="123456789123456")
    db.session.add(default_user)
    db.session.add(second_user)
    db.session.commit()

    location1 = Location("Praha", default_user)
    location2 = Location("Brno", default_user)
    location3 = Location("Liberec", second_user)

    db.session.add(location1)
    db.session.add(location2)
    db.session.add(location3)
    db.session.commit()
    yield

    db.drop_all()
