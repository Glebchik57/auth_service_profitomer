import sqlalchemy as db
from werkzeug.security import (generate_password_hash, check_password_hash)
from flask_login import UserMixin

from db_config import Base, engine


class Users(Base, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    tg_id = db.Column(db.Integer, unique=True)
    tg_username = db.Column(db.String(100))
    phone = db.Column(db.BigInteger, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    surname = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(200), nullable=False)
    active = db.Column(db.SmallInteger)
    date_start = db.Column(db.Integer)
    date_end = db.Column(db.Integer)
    a_code = db.Column(db.Text)
    wb_token = db.Column(db.Text)
    tax_rate = db.Column(db.Integer)

    def set_password(self, password):
        '''Установка хэша пароля'''
        self.password = generate_password_hash(password)

    def check_password(self, password):
        '''Проверка хэша пароля'''
        return check_password_hash(self.password, password)


class Sessions(Base):
    __tablename__ = "sessions"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    ip = db.Column(db.Integer, nullable=False)
    date_start = db.Column(db.Integer)
    date_end = db.Column(db.Integer)


Base.metadata.create_all(engine)
