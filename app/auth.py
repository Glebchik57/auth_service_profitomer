from datetime import datetime

from flask import request
from flask_login import user_logged_in, user_logged_out

from models import Sessions
from db_config import session


def track_login(sender, user, **extra):
    '''Сохранение времени входа пользователя'''
    ses = Sessions(
        user_id=user.id,
        ip=request.remote_addr,
        date_start=datetime.now()
    )
    session.add(ses)
    session.commit()


def track_logout(sender, user, **extra):
    '''Сохранение выхода пользователя из профиля'''
    ses = session.query(Sessions).filter_by(
        user_id=user.id,
        date_end=None
    ).first()
    if ses:
        ses.date_end = datetime.now()
        session.commit()


user_logged_in.connect(track_login)  # отслеживание события входа пользователя
user_logged_out.connect(track_logout)  # отслеживание события выхода пользователя
