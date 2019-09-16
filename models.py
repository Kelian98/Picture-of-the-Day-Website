from datetime import datetime

from app import db


class Submitted(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_posted = db.Column(db.DateTime, nullable=False,
                            default=datetime.utcnow)
    firstname = db.Column(db.String(30), unique=False, nullable=False)
    lastname = db.Column(db.String(30), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=False, nullable=False)
    website = db.Column(db.String(50), unique=False, nullable=False)
    picture_title = db.Column(db.String(50), nullable=False,
                              default='default.jpg')
    description = db.Column(db.String(1000), unique=False, nullable=False)

    def __repr__(self):
        return f"Post('{self.date_posted}', '{self.firstname}', '{self.lastname}', '{self.picture_title}')"
