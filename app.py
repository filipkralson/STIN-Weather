from flask import Flask
from dotenv import load_dotenv
from project.controller.main import main
from project.controller.user import user
from project.controller.payment import payment_bp
from project.utils.database import db
import os


def create_app():
    app = Flask(__name__, template_folder='project/templates')

    config_type = os.getenv('CONFIG_TYPE', default='config.DevelopmentConfig')
    app.config.from_object(config_type)

    db.init_app(app)

    with app.app_context():
        db.create_all()

    app.register_blueprint(main)
    app.register_blueprint(user)
    app.register_blueprint(payment_bp)

    return app


if __name__ == '__main__':
    app = create_app()
    app.run()
