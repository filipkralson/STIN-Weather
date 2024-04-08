from flask import Flask
from dotenv import load_dotenv
from controller.main import main
from controller.user import user
from controller.payment import payment_bp
from utils.database import db
import os


def create_app():
    load_dotenv(dotenv_path=".env")

    app = Flask(__name__, template_folder='templates')
    app.config["SECRET_KEY"] = os.getenv("KEY")
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DB_LOGIN")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    with app.app_context():
        db.create_all()

    app.register_blueprint(main)
    app.register_blueprint(user)
    app.register_blueprint(payment_bp)

    return app


if __name__ == '__main__':
    create_app().run(debug=True)
