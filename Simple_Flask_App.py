import os
from flask import Flask, render_template, redirect, url_for, request, send_from_directory
from flask_login import LoginManager, login_required, login_user, logout_user, current_user

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ExtraSecureSecretKey'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login_page'

class AdventureUser(UserMixin):
    pass

registered_users = {'EnduroFreak': {'password': 'Enduro2023'}}

@login_manager.user_loader
def load_user(user_name):
    if user_name not in registered_users:
        return
    enduro_user = AdventureUser()
    enduro_user.id = user_name
    return enduro_user

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
    if request.method == 'POST' and (user_name in registered_users) and (request.form['password'] == registered_users[user_name]['password']):
        enduro_user = AdventureUser()
        enduro_user.id = user_name
        login_user(enduro_user)
        return redirect(url_for('protected_area'))

@app.route('/protected')
@login_required
def protected_area():
    if current_user.is_authenticated:
        return 'Welcome back, ' + current_user.id + '! Ready for a new adventure?'
    else:
        return redirect(url_for('login_page'))

@app.route('/logout')
@login_required
def logout_user():
    logout_user()
    return redirect(url_for('login_page'))

if __name__ == "__main__":
    app.run(port=5000, debug=True)

    app.run(port=5000, debug=True)


