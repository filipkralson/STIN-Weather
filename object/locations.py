from utils.database import db


class Location(db.Model):
    id = db.Column("location_id", db.Integer, primary_key=True)
    location = db.Column(db.String(100))
    user_id = db.Column(db.Integer, db.ForeignKey("user.user_id"))

    def __init__(self, location, user):
        self.location = location
        self.user = user
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()

    def delete_location(self):
        try:
            db.session.delete(self)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            return False
