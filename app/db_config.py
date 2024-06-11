import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from dotenv import load_dotenv


load_dotenv()


NAME = os.getenv('NAME')
PASSWORD = os.getenv('PASSWORD')
HOST = os.getenv('HOST')
PORT = os.getenv('PORT')
DB = os.getenv('DB')


DATABASE_URI = (
    f'postgresql+psycopg2://{NAME}:{PASSWORD}@{HOST}:{PORT}/{DB}'
)


class Base(DeclarativeBase):
    pass


engine = create_engine(DATABASE_URI)

Session = sessionmaker(bind=engine)
session = Session()
