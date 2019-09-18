from sqlalchemy import Column, Integer, String, DateTime
from database import Database as Model

from datetime import datetime

class Submitted(Model):
    __tablename__ = 'submitted'
    id = Column(Integer, primary_key=True)
    date_posted = Column(DateTime, nullable=False,
                            default=datetime.utcnow)
    firstname = Column(String(30), unique=False, nullable=False)
    lastname = Column(String(30), unique=False, nullable=False)
    email = Column(String(120), unique=False, nullable=False)
    website = Column(String(50), unique=False, nullable=False)
    picture_title = Column(String(50), nullable=False,
                              default='default.jpg')
    description = Column(String(1000), unique=False, nullable=False)

    def __repr__(self):
        return f"Post('{self.date_posted}', '{self.firstname}', '{self.lastname}', '{self.picture_title}')"
