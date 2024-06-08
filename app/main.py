from flask import (
    Flask,
    redirect,
    render_template,
    request,
    session,
    url_for,
    flash
)
from werkzeug.security import (generate_password_hash, check_password_hash)

from flask_login import LoginManager, current_user, login_user, login_required, logout_user

from models import Users
from forms import AutorizationForm, RegistrationForm, ChangePasswordForm, SetPasswordForm, TaxRateForm
from db_config import session
from sg_maillib import SG_mail


app = Flask(__name__)
app.config['SECRET_KEY'] = 'b\\x18*\xef}\xe6\xf0\xacjXk!,\ty\tH\x14\xf6u\xc4\xcd\xa2\x99.'

login_manager = LoginManager(app)
login_manager.login_view = 'autorization'

mail = SG_mail()


@login_manager.user_loader
def load_user(users_id):
    return session.query(Users).get(users_id)


@app.route('/')
@login_required
def index():
    try:
        user = current_user.name
        return render_template('base_template.html', name=user)
    except Exception as error:
        return render_template('base_template.html', name=f'что-то пошло не так{error}')


@app.route("/autorization", methods=['GET', 'POST'])
def autorization():
    form = AutorizationForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        user = session.query(Users).filter_by(email=email).first()
        if not user:
            flash('Неверный email.')
            return redirect(url_for('autorization'))
        if user.active != 1:
            flash('Ваш аккаунт не активирован. Проверьте почту')
            return redirect(url_for('autorization'))
        else:
            if check_password_hash(user.password, password):
                login_user(user)
                return redirect(url_for('index'))
            else:
                flash('Неверный пароль.')
                return redirect(url_for('autorization'))
    else:
        return render_template('autorization.html', form=form)


@app.route("/registration", methods=['GET', 'POST'])
def registration():
    form = RegistrationForm()
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
                    body_text = " Ссылка для активации аккаунта: https://profitomer.ru/activation?code=" + a_code
                    mail.send_email("Profitomer.ru активация аккаунта", email, body_text)
                    return render_template('div_after_registration.html', email=email)
                except Exception:
                    session.rollback()
                    flash('Ошибка регистрации', 'danger')
                    return render_template('registration.html', form=form)
    else:
        return render_template('registration.html', form=form)




@app.route("/activation", methods=['GET', 'POST'])
def activation():
    if request.args.get('code'):
        try:
            a_code = request.args.get('code')
            user = session.query(Users).filter_by(a_code=a_code).first()
            if user:
                user.active = 1
                session.add(user)
                session.commit()
                return "Активация аккаунта прошла успешно!<br> <a href='/'>Перейти в личный кабинет</a>"
            else:
                return "Некорректный код активации"
        except Exception as error:
            return f'Ошибка запроса данных! {error}'
    else:
        return "Некорректный запрос."


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Вы вышли из своего профиля')
    return redirect(url_for('index'))


@app.route('/tax_rate_change', methods=['POST'])
@login_required
def change_tax_rate():
    form = TaxRateForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            user = current_user
            user.tax_rate = form.tax_rate.data
            session.commit()
            return redirect(url_for('index'))
    else:
        return render_template('tax_rate_change.html', form=form)
    


@app.route("/change_password", methods=['GET', 'POST'])
@login_required
def change_password():
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
                user.password = generate_password_hash(new_password)
                session.commit()
                return redirect(url_for('index'))
    else:
        return render_template('change_password.html', form=form)


@app.route('/new-password', methods=['GET', 'POST'])
def set_new_password():
    form = SetPasswordForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            email = form.email.data
            if session.query(Users).filter_by(email=email).first() is not None:
                user = session.query(Users).filter_by(email=email).first()
                new_password = mail.generate_unique_id(8)
                user.password = generate_password_hash(new_password)
                session.commit()
                body_text = f'Ваш новый пароль: {new_password}'
                mail.send_email("Profitomer.ru смена пароля", email, body_text)
                flash('Пароль был успешно изменен')
                return redirect(url_for('autorization'))
            else:
                flash(f'Пользователя с email {email} не существует')
                render_template('set_new_password.html', form=form)
    else:
        render_template('set_new_password.html', form=form)


if __name__ == "__main__":
    app.run(debug=True)
