'''Пакет app является основным для приложения AUTH_SERVICE_PROFITOMER.
Предназначен для авторизации и аутентификации пользователей,
фиксирует вход и выход пользователей из их аккаунтов.
Так же позволяет пользователям менят пароль от их учетной записи
и менять величину налоговой ставки.'''

import os

from flask import Flask

from flask_login import LoginManager
from dotenv import load_dotenv


load_dotenv()


app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

login_manager = LoginManager(app)
login_manager.login_view = 'autorization'

from . import views
