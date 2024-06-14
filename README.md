# auth_service_profitomer
## Описание:
Проект регистрации и аунтефикации пользователей для проекта Profitomer.ru

Сервис позволяет:
- Регестрировать пользователей
- Аунтефикация пользователей
- Смена пароля
- Изменение налоговой ставки
- Фиксация времени входа и выхода пользователя из аккаунта

## Стек технологий
- Python 3.11
- Flask 2.3.3
- Flask-Login 0.6.3
- SQLAlchemy 2.0.30
- alembic 1.13.1

## Запуск проекта
- Сделать форк репозитория https://github.com/Glebchik57/auth_service_profitomer
- Склонировать репозиторий на свой компьютер
```
git clone ...
```
- Cоздать и активировать виртуальное окружение
```
python -m venv venv
source venv/Scripts/activate
```
- Установить зависимости из файла requirements.txt

```
python -m pip install --upgrade pip
pip install -r requirements.txt
```
- создать файл .env
```
touch .env
```
- Внести в файл .env информации в соответствии с .env.example
- Выполнить миграции
1. Инициализировать Alembic

```
alembic init alembic

```
2. Настроить alembic.ini и alembic/env.py
3. Создать миграции
```
alembic revision --autogenerate -m "описание миграции"
```
4. Применить миграции
```
alembic upgrade head

```

- Запустить проект

```
python app.py
```

## Автор
[Sevostyanov Gleb](https://github.com/Glebchik57)