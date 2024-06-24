from flask import Flask, render_template, redirect, url_for, request, session, flash
from flask_sqlalchemy import SQLAlchemy
from forms.login_form import LoginForm
from forms.registration_form import RegistrationForm

app = Flask(__name__)
app.secret_key = 'fgsgdrgidfs'

# configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# initialize the SQLAlchemy extension
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=True)


# create the database and tables
with app.app_context():
    db.create_all()


@app.route("/")
def home():
    return render_template('home.html')


@app.route("/users")
def users():
    users_list = User.query.all()
    return render_template('users.html', users_list=users_list)


@app.route("/users/<string:username>")
def show_user(username):
    if 'username' in session and session['username'] == username:
        return render_template('user.html', username=username)
    return redirect(url_for('login'))


@app.route("/posts")
def posts():
    return render_template('posts.html', posts=range(1, 11))


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username, password=password).first()
        if user:
            session['username'] = username
            flash(f'Вітаємо {username}! ви успішно авторизувалися!')
            return redirect(url_for('show_user', username=username))
        else:
            flash('Невірний логін або пароль.')

    return render_template('login.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        username = request.form['username']
        password = request.form['password']

        existing_user = User.query.filter_by(username=username).first()
        if existing_user is None:
            new_user = User(username=username, password=password)
            db.session.add(new_user)
            db.session.commit()
            session['username'] = username
            flash(f"Вітаю {username}! Ви успішно зареєструвались!")
            return redirect(url_for('show_user', username=username))
        else:
            flash(f"Користувач з іменем {username} вже існує. Будь ласка, виберіть інше ім'я.")
    return render_template('register.html', form=form)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))


@app.route('/profile')
def profile():
    if 'username' in session:
        username = session['username']
        return render_template('user.html', username=username)
    return redirect(url_for('login'))


if __name__ == "__main__":
    app.run(debug=True, port=8000)
