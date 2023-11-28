from flask import Flask, render_template
from flask_migrate import Migrate
import config
from exts import db
from models import *
from forms import Login
from flask import Flask, request, render_template, jsonify, flash, redirect, url_for, g, session
from bluePrints.user import user
from bluePrints.book import book
from bluePrints.admin import admin

app = Flask(__name__)

# bind config file
app.config.from_object(config)

db.init_app(app)

migrate = Migrate(app, db)

app.register_blueprint(user)
app.register_blueprint(book)
app.register_blueprint(admin)

@app.route('/')
def hello_world():  # put application's code here
    form = Login()
    return render_template("login.html", form=form)

# the route to log in
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        form = Login()
        return render_template('login.html', form=form)
    elif request.method == 'POST':
        form = Login()
        if form.validate_on_submit():
            account = UserModel.query.filter_by(account_name=form.account.data, password=form.password.data).first()
            if account is None:
                flash(u'Wrong user name or password！')
                # unicode
                return redirect(url_for('login'))
            else:
                session['account_id'] = account.account_name
                print("login success!")
                if account.auth_type==1:
                    print("admin login")
                    return redirect(url_for('admin.index'))
                return redirect(url_for('book.list'))
# log out: clean the session
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

# a global variable g, powerful!!!!
@app.before_request
def before_login():
    account_id = session.get('account_id')
    if account_id:
        account = UserModel.query.filter_by(account_name=account_id).first()
        setattr(g, 'account', account)
    else:
        setattr(g, 'account', None)
# if login, use g to save the account
if __name__ == '__main__':
    app.run()
