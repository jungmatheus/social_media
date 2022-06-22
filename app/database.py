from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings as s

SQLALCHEMY_DATABASE_URL = f'postgresql://{s.DATABASE_USERNAME}:{s.DATABASE_PASSWORD}@{s.DATABASE_HOSTNAME}/social_media'
engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        print('connected')
        yield db
    finally:
        db.close()
