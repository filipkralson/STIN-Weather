import pytest
from flask import Flask
from utils.database import db

@pytest.fixture
def app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    # Propojení instance SQLAlchemy s aplikací Flask
    db.init_app(app)
    return app

def test_db_configured(app):
    with app.app_context():
        # Test, zda instance db má správně nastavenou URI databáze
        assert db.engine.url.drivername == 'sqlite'
