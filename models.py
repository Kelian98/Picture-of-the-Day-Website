from sqlalchemy import Column, Integer, String, DateTime, Date
from database import Database as Base

from datetime import datetime

class Model():

    def save(self):
        from database import db_session

        db_session.add(self)
        db_session.commit()

class Submitted(Base, Model):
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
    picture = Column(String(1000), unique=True, nullable=False)
    published = Column(Date, nullable=True, default=None)

    IMAGE_ALLOWED = ['jpg', 'png', 'jpeg', 'tiff']

    def __repr__(self):
        return f"Post('{self.date_posted}', '{self.firstname}', '{self.lastname}', '{self.picture_title}')"

def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind migrate_engine
    # to your metadata
    Base.metadata.bind = migrate_engine
    Base.__table__.create(migrate_engine)

def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    Base.metadata.bind = migrate_engine
    Base.__table__.drop(migrate_engine)
