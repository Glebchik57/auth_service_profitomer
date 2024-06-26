import time
import ipaddress

from flask import (
    redirect,
    render_template,
    request,
    url_for,
    flash
)
from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)
from flask_login import (
    current_user,
    login_user,
    login_required,
    logout_user
)

from app import app
from app.models import Users, Sessions
from .forms import (
    AutorizationForm,
    RegistrationForm,
    ChangePasswordForm,
    SetPasswordForm,
    TaxRateForm
)
from db_config import session
from sg_maillib import SG_mail


mail = SG_mail()


@app.route('/')
@login_required
def index():
    '''Тестовое представления главной страницы'''

    try:
        user = current_user.name
        id = current_user.id
        return render_template('base_template.html', name=id)
    except Exception as error:
        return render_template(
            'base_template.html',
            name=f'что-то пошло не так{error}'
        )


@app.route("/autorization", methods=['GET', 'POST'])
def autorization():
    '''Представление авторизации.
    Включает проверку авторизации пользователя, валидации формы,
    активации пользователя, соответствия пароля,
    фиксация времени подключения пользователя к сессии'''

    form = AutorizationForm()
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    else:
        if form.validate_on_submit():
            email = form.email.data
            password = form.password.data
            user = session.query(Users).filter_by(email=email).first()
            if not user:
                flash('Неверный email.', 'warning')
                return redirect(url_for('autorization'))
            if user.active != 1:
                flash('Ваш аккаунт не активирован. Проверьте почту', 'warning')
                return redirect(url_for('autorization'))
            else:
                if check_password_hash(user.password, password):
                    ip = request.environ.get(
                        'HTTP_X_FORWARDED_FOR',
                        request.remote_addr
                    )
                    ses = Sessions(
                        user_id=user.id,
                        ip=int(ipaddress.IPv4Address(ip)),
                        date_start=time.time()
                    )
                    session.add(ses)
                    session.commit()
                    login_user(user, remember=True)
                    return redirect(url_for('index'))
                else:
                    flash('Неверный пароль.', 'warning')
                    return redirect(url_for('autorization'))
        else:
            return render_template('autorization.html', form=form)


@app.route("/registration", methods=['GET', 'POST'])
def registration():
    '''Представление регистрации.
    Включает в себя проверку аворизации пользователя, валидации формы,
    наличия в бд пользователей с аналогичными полями(email, tg, phone).
    После успешной проверки отправляет на почту ссылку для активации.'''

    form = RegistrationForm()
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    else:
        if request.method == 'POST':
            if form.validate_on_submit():
                email = form.email.data
                tg = form.tg.data
                phone = form.phone.data
                name = form.name.data
                surname = form.surname.data
                password = form.password.data
                a_code = mail.generate_unique_id(16)
                if session.query(Users).filter_by(email=email).first():
                    flash(
                        f'Пользователь с почтой {email} уже существует',
                        'warning'
                    )
                    return render_template('registration.html', form=form)
                elif session.query(Users).filter_by(tg_username=tg).first():
                    flash(
                        f'Пользователь с telegram ником {tg} уже существует',
                        'warning'
                    )
                    return render_template('registration.html', form=form)
                elif session.query(Users).filter_by(phone=phone).first():
                    flash(
                        f'Пользователь с номером {phone} уже существует',
                        'warning'
                    )
                    return render_template('registration.html', form=form)
                else:
                    try:
                        new_user = Users(
                            email=email,
                            phone=phone,
                            tg_username=tg,
                            name=name,
                            surname=surname,
                            password=generate_password_hash(password),
                            a_code=a_code
                        )
                        session.add(new_user)
                        session.commit()
                        link = (
                            f'https://profitomer.ru/activation?code={a_code}'
                        )
                        body_text = f'Ссылка для активации аккаунта: {link}'
                        mail.send_email(
                            "Profitomer.ru активация аккаунта",
                            email,
                            body_text
                        )
                        return render_template(
                            'div_after_registration.html',
                            email=email
                        )
                    except Exception:
                        session.rollback()
                        flash('Ошибка базы данных. Попробуйте позже', 'error')
                        return render_template('registration.html', form=form)
        else:
            return render_template('registration.html', form=form)


@app.route("/activation", methods=['GET', 'POST'])
def activation():
    '''Представление активации аккаунта пользователя.
    Включает в себя проверку соответствия кода активации.'''

    if request.args.get('code'):
        a_code = request.args.get('code')
        user = session.query(Users).filter_by(a_code=a_code).first()
        if user:
            try:
                user.active = 1
                session.add(user)
                session.commit()
                return "Активация аккаунта прошла успешно!<br> <a href='/'>Перейти в личный кабинет</a>"
            except Exception:
                session.rollback()
                return 'Ошибка базы данных'
        else:
            return "Некорректный код активации"
    else:
        return "Некорректный запрос."


@app.route('/logout')
@login_required
def logout():
    '''Представление выхода из профиля.
    Включает в себя определение текущей сессии в
    таблице sessions и добавление в запись
    времени окончания сессии'''

    user = current_user
    ses = session.query(Sessions).filter_by(
        user_id=user.id,
        date_end=None
    ).first()
    if ses:
        ses.date_end = time.time()
        session.commit()
    logout_user()
    flash('Вы вышли из своего профиля', 'info')
    return redirect(url_for('index'))


@app.route('/tax_rate_change', methods=['GET', 'POST'])
@login_required
def change_tax_rate():
    '''Представление изменения налоговой ставки.
    Включает в себя проверку валидации формы.'''

    form = TaxRateForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            try:
                user = current_user
                user.tax_rate = form.tax_rate.data
                session.commit()
                return redirect(url_for('index'))
            except Exception:
                flash('Ошибка базы данных', 'error')
                return redirect(url_for('change_tax_rate'))
    else:
        return render_template('tax_rate_change.html', form=form)


@app.route("/change_password", methods=['GET', 'POST'])
@login_required
def change_password():
    '''Представление изменения пароля аутентификацированного пользователя.
    Включает в себя проверку валидации формы и правильного введения пароля.'''

    form = ChangePasswordForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            user = current_user
            old_password = form.old_password.data
            new_password = form.new_password.data
            rp_new_password = form.rp_new_password.data
            if not check_password_hash(user.password, old_password):
                flash('Введенный пароль не соответствует текущему')
                return redirect(url_for('change_password'))
            elif new_password != rp_new_password:
                flash(
                    'Повторно ввыеденный пароль не соответсвует новому паролю'
                )
                return redirect(url_for('change_password'))
            else:
                try:
                    user.password = generate_password_hash(new_password)
                    session.commit()
                    return redirect(url_for('index'))
                except Exception:
                    flash('Ошибка базы данных', 'error')
                    return redirect(url_for('change_password'))
    else:
        return render_template('change_password.html', form=form)


@app.route('/new-password', methods=['GET', 'POST'])
def set_new_password():
    '''Представление изменения пароля неаутентификацированного пользователя.
    Включает в себя проверку валидации формы и существования пользователя
    с указанным email. Самостоятельно генерирует новый пароль и направляет
    на указанный email'''
    form = SetPasswordForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            email = form.email.data
            if session.query(Users).filter_by(email=email).first() is not None:
                try:
                    user = session.query(Users).filter_by(email=email).first()
                    new_password = mail.generate_unique_id(8)
                    user.password = generate_password_hash(new_password)
                    session.commit()
                    body_text = f'Ваш новый пароль: {new_password}'
                    mail.send_email(
                        "Profitomer.ru смена пароля",
                        email,
                        body_text
                    )
                    flash('Пароль был успешно изменен')
                    return redirect(url_for('autorization'))
                except Exception:
                    flash('Ошибка базы данных', 'error')
                    return redirect(url_for('set_new_password'))
            else:
                flash(f'Пользователя с email {email} не существует')
                return render_template('set_new_password.html', form=form)
    else:
        return render_template('set_new_password.html', form=form)
