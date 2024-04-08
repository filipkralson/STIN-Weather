from werkzeug.security import generate_password_hash, check_password_hash
from object.locations import Location
from utils.database import db


class User(db.Model):
    id = db.Column("user_id", db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    password = db.Column(db.String(200))
    isSubscribed = db.Column(db.Boolean, default=False)
    card_number = db.Column(db.String(16))
    towns = db.relationship("Location", backref="user", lazy="dynamic", cascade="all, delete-orphan")

    def __init__(self, name, password, card_number):
        self.name = name
        self.setPasswd(password)  
        self.isSubscribed = False
        self.card_number = card_number

    def add(self, name):
        new_town = Location(name, self)
        db.session.add(new_town)
        db.session.commit()

    def setPasswd(self, password):
        self.password = generate_password_hash(password)

    def checkPasswd(self, password):
        return check_password_hash(self.password, password)

    def setIsSubscribed(self, subscribed):
        self.isSubscribed = subscribed
        db.session.commit()

    def getSubscribed(self):
        return self.isSubscribed


def getUser(name):
    return User.query.filter_by(name=name).first()
