from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base


SQLITE_URI = 'sqlite:///upod.db'

engine = create_engine(SQLITE_URI, convert_unicode=True)

Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db_session = scoped_session(Session)

Database = declarative_base()
Database.query = db_session.query_property()

def init_db():
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()
    from models import Submitted
    Database.metadata.create_all(bind=engine)
