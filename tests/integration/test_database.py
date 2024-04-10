from project.utils.database import db


def test_db_configured(app):
    with app.app_context():
        assert db.engine.url.drivername == 'sqlite'
