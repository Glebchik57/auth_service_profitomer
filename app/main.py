from flask import (
    Flask,
    redirect,
    render_template,
    request,
    session,
    url_for,
    flash
)
from flask_login import LoginManager, current_user, login_required

from models import Users
from forms import AutorizationForm, RegistrationForm
from db_config import session


app = Flask(__name__)
app.config['SECRET_KEY'] = 'b\\x18*\xef}\xe6\xf0\xacjXk!,\ty\tH\x14\xf6u\xc4\xcd\xa2\x99.'

login_manager = LoginManager(app)
login_manager.login_view = 'autorization'


@login_manager.user_loader
def load_user(user_id):
    return session.query(Users).get(user_id)


@app.route('/')
@login_required
def index():
    return render_template('base_template.html', name='Ксюша')


@app.route("/autorization", methods=['GET', 'POST'])
def autorization():
    form = AutorizationForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        print(email)
        print(password)
        # здесь логика базы данных
        print("\nData received. Now redirecting ...")
        return redirect(url_for('autorization'))

    return render_template('autorization.html', form=form)


@app.route("/registration", methods=['GET', 'POST'])
def registration():
    form = RegistrationForm
    if request.method == 'POST':
        if form.validate_on_submit():
            email = request.form['email']
            tg =  request.form['tg']
            phone = request.form['email']
            name = request.form['email']
            surname = request.form['email']
            password = request.form['email']
            if Users.query.filter_by(email=email).first():
                flash(
                    f'Пользователь с почтой {email} уже существует',
                    'warning'
                )
                return render_template('autorization.html')
            if Users.query.filter_by(tg_username=tg).first():
                flash(
                    f'Пользователь с telegram ником {tg} уже существует',
                    'warning'
                )




@app.route("/activation", methods=['GET', 'POST'])
def activation():
    pass


@app.route('/tax_rate_change', methods=['POST'])
@login_required
def change_tax_rate():
    pass


@app.route("/change_password", methods=['GET', 'POST'])
@login_required
def change_password():
    pass


@app.route('/new-password', methods=['GET', 'POST'])
def set_new_password():
    pass


@app.route('/logout')
@login_required
def logout():
    pass


if __name__ == "__main__":
    app.run(debug=True)
