from flask import Flask, redirect, url_for, request, render_template, flash, send_from_directory
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
import os

app = Flask(__name__)
app.config.from_object('config.Config')

# Initialize the database
db = SQLAlchemy(app)

# Set up Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login_page'

# Define the User model
class User(UserMixin, db.Model):
    id = db.Column(db.String(80), primary_key=True)
    password_hash = db.Column(db.String(128))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
        
with app.app_context():
    db.create_all()

# Define the user loader for Flask-Login
@login_manager.user_loader
def load_user(user_name):
    return User.query.get(user_name)

# Define the main page route
@app.route('/')
def main_page():
    return redirect(url_for('login_page'))

# Define a route for the favicon
@app.route('/favicon.ico')
def show_favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.png', mimetype='image/png')

# Define the login page route
@app.route('/login', methods=['GET', 'POST'])
def login_page():
    if request.method == 'POST':
        user_name = request.form['username']
        password = request.form['password']
        user = User.query.get(user_name)
        if user is not None and user.check_password(password):
            login_user(user)
            return redirect(url_for('protected_area'))
        else:
            flash("Invalid username or password")
    return render_template('login.html')

# Define the registration page route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        user_name = request.form['username']
        password = request.form['password']
        if User.query.get(user_name) is not None:
            flash("Username already exists")
        else:
            new_user = User(id=user_name)
            new_user.set_password(password)
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('login_page'))
    return render_template('register.html')

# Define a protected route that requires login
@app.route('/protected')
@login_required
def protected_area():
    return "You have logged in successfully"

if __name__ == '__main__':
    app.run(debug=True)

   


