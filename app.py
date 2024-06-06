from flask import Flask, render_template, redirect, url_for, request, session, flash

app = Flask(__name__)
app.secret_key = 'fgsgdrgidfs'

user_database = {
    "roman": "123456",
    "viktory": "qwerty",
}


@app.route("/")
def home():
    return render_template('home.html')


@app.route("/users")
def users():
    users_list = [
        {"name": 'Роман', "username": 'roman'},
        {"name": 'Вікторія', "username": 'viktory'},
    ]
    return render_template('users.html', users_list=users_list)


@app.route("/users/<string:username>")
def show_user(username):
    if 'username' in session and session['username']:
        return render_template('user.html', username=username)
    return redirect(url_for('login'))


@app.route("/posts")
def posts():
    return render_template('posts.html', posts=range(1, 11))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username in user_database and user_database[username] == password:
            session['username'] = username
            flash(f'Вітаємо {username}!ви успішно авторизувалися!')

            return redirect(url_for('show_user', username=username))

    return render_template('login.html')


@app.route('/register')
def register():
    return render_template('register.html')


@app.route('/about')
def about():
    return render_template('about.html')



@app.route('/logout')
def logout():
    session.pop('username', None)

    return redirect(url_for('home'))

@app.route('/profile')
def profile():
    return render_template('user.html')

if __name__ == "__main__":
    app.run(debug=True, port=8000)
