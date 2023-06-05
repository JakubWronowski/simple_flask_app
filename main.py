from flask import Flask, redirect, url_for, request, render_template, send_from_directory
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
import os

app = Flask(__name__)
app.config.from_object('config.Config')


db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login_page'

class User(UserMixin, db.Model):
    id = db.Column(db.String(80), primary_key=True)
    password_hash = db.Column(db.String(128))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

@login_manager.user_loader
def load_user(user_name):
    return User.query.get(user_name)

@app.route('/')
def main_page():
    return redirect(url_for('login_page'))

@app.route('/favicon.ico')
def show_favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.png', mimetype='image/png')

@app.route('/login', methods=['GET', 'POST'])
def login_page():
    if request.method == 'GET':
        return render_template('login.html')
    user_name = request.form['username']
    password = request.form['password']
    user = User.query.get(user_name)
    if user is not None and user.check_password(password):
        login_user(user)
        return redirect(url_for('protected_area'))
    else:
        return redirect(url_for('login_page'))  # You should probably show some error message here

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        user_name = request.form['username']
        password = request.form['password']
        if User.query.get(user_name) is not None:
            return 'User already exists'  # You should probably show some error message here
        new_user = User(id=user_name)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login_page'))
    return render_template('register.html')

@app.route('/protected')
@login_required
def protected_area():
    return 'Welcome back, ' + current_user.id + '! Ready for a new adventure?'

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login_page'))

if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # This will create the database if it does not exist yet
    app.run(port=5000, debug=True)


   


