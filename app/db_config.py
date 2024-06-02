from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase


DATABASE_URI = 'postgresql+psycopg2://postgres:postgres@localhost:5432/postgres'

class Base(DeclarativeBase):
    pass


engine = create_engine(DATABASE_URI)

Session = sessionmaker(bind=engine)
session = Session()
