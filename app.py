from flask import Flask
from dotenv import load_dotenv
from project.controller.main import main
from project.controller.user import user
from project.controller.payment import payment_bp
from project.utils.database import db
import os


def create_app(option):
    app = Flask(__name__, template_folder='project/templates')
    load_dotenv(dotenv_path=".env")

    if option == "test":
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        constring = 'sqlite:///:memory:'
    else:
        constring = os.getenv("DB_LOGIN")

    app.config["SECRET_KEY"] = os.getenv("KEY")
    app.config["SQLALCHEMY_DATABASE_URI"] = constring
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    with app.app_context():
        db.create_all()

    app.register_blueprint(main)
    app.register_blueprint(user)
    app.register_blueprint(payment_bp)

    return app


if __name__ == '__main__':
    create_app("").run(debug=True)
