from flask import Flask
from controller.main import post, get, weather, add_to_favourite


def create_test_app():
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False  # Disable CSRF protection for testing
    return app


def test_main_post():
    pass


def test_main_get():
    pass


def test_main_weather():
    pass


def test_main_add_to_favourite():
    pass
