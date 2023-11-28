from forms import RegisterForm
from models import UserModel
from flask import Blueprint, render_template, request, url_for, session, redirect, jsonify, flash, g, make_response
from exts import db
from datetime import datetime
from forms import Login


# __name__ is current module
user = Blueprint('user', __name__)

def now_time():
    now = datetime.now()
    formatted_time = str(now.strftime("%Y-%m-%d %H:%M:%S"))
    return formatted_time

def get_current_user():
    account_id = session.get('account_id')
    account = None
    if account_id:
        account = UserModel.query.filter_by(account_name=account_id).first()
    return account

# logout redirect
@user.route('/user/logout')
def logout():
    return redirect(url_for('login'))

# how to register
@user.route('/user/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        form = RegisterForm()
        return render_template("register.html", form=form)
    # get request,return the page
    # post request, get the data, do some actions, sometimes need response
    elif request.method == 'POST':
        form = RegisterForm()
        if form.validate_on_submit():
            print("validate_on_submit trigger")
            account = UserModel.query.filter_by(account_name=form.account.data).first()
            # sorry, account unique name is suitable
            if account is not None:
                flash(u'The account id already exists')
                return render_template("register.html", form=form)
            else:
                if form.password.data != form.repeat_password.data:
                    flash(u'The password must be the same')
                    return render_template("register.html", form=form)
                u = UserModel()
                u.username = form.user_name.data
                u.account_name = form.account.data
                u.password = form.password.data
                now = datetime.now()
                formatted_time = str(now.strftime("%Y-%m-%d %H:%M:%S"))
                u.create_time = formatted_time
                u.update_time = formatted_time
                u.auth_type = 2
                db.session.add(u)
                db.session.commit()
                flash(f'account:\'{form.account.data}\' register successfully')
                return redirect(url_for('login'))
        return render_template("register.html", form=form)

# login page
@user.route('/user/login', methods=['GET', 'POST'])
def login():
    form = Login()
    return render_template("login.html", form=form)

# add the user
@user.route('/user/add_user', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        # 获取表单数据
        username = request.form['username']
        account_number = request.form['account_number']
        password = request.form['password']

        print(f"username:{username},account_number:{account_number},password:{password}")

        account = UserModel.query.filter_by(account_name=account_number).first()
        if account is not None:
            flash(u'The account id already exists')
            return render_template('admin-addadmin.html', account=get_current_user())

        us = UserModel()
        us.username = username
        us.account_name = account_number
        us.password = password
        us.create_time = us.update_time=now_time()
        us.auth_type = 2

        db.session.add(us)
        db.session.commit()
        flash(f'user account {account_number} register successfully')

        return render_template('admin-adduser.html', account=get_current_user())

# add admin
@user.route('/user/add_admin', methods=['GET', 'POST'])
def add_admin():
    if request.method == 'POST':
        # 获取表单数据
        username = request.form['username']
        account_number = request.form['account_number']
        password = request.form['password']

        account = UserModel.query.filter_by(account_name=account_number).first()
        if account is not None:
            flash(u'The account id already exists')
            return render_template('admin-addadmin.html', account=get_current_user())

        us = UserModel()
        us.username=username
        us.account_name=account_number
        us.password=password
        us.create_time=us.update_time=now_time()
        us.auth_type=1

        db.session.add(us)
        db.session.commit()
        flash(f'admin account {account_number} register successfully')

        return render_template('admin-addadmin.html', account=get_current_user())

# update the information of user
@user.route('/user/update_user', methods=['GET', 'POST'])
def update_user():
    if request.method == 'POST':
        # get the information
        username = request.form['username']
        account_number = request.form['account_number']
        password = request.form['password']

        account = UserModel.query.filter_by(account_name=account_number).first()
        if account is None:
            flash(u'The account id is none')
            return render_template('admin-update_user.html', account=get_current_user())

        if username is not None and username.strip()!='':
            account.username=username
        if password is not None and password.strip()!='':
            account.password=password
        db.session.commit()
        flash(f'update account {account_number} successfully')
    return render_template('admin-update_user.html', account=get_current_user())

# delete all the users
@user.route('/user/delete_user', methods=['GET', 'POST'])
def delete_user():
    account_number = request.form['account_number']
    account = UserModel.query.filter_by(account_name=account_number).first()
    if account is None:
        flash(u'The account id is none')
        return render_template('admin-update_user.html', account=get_current_user())
    print(f"account:{account.to_dict()}")
    db.session.delete(account)
    db.session.commit()
    flash(f'delete account {account.account_name} successfully')
    return render_template('admin-update_user.html', account=get_current_user())

# get users selected
@user.route('/user/list_query', methods=['GET', 'POST'])
def list_query():
    content = request.args.get('content')
    method = request.args.get('method')

    print(f"content:{content},method:{method}")
    us = None
    if method=='username':
        us = UserModel.query.filter(UserModel.username.like('%'+content+'%')).all()
    elif method == 'account_name':
        us = UserModel.query.filter(UserModel.account_name.like('%'+content+'%')).all()
    elif method == 'type':
        us = UserModel.query.filter(UserModel.auth_type.like('%'+content+'%')).all()
    if method==None or content==None or content.strip() =='':
        us = UserModel.query.all()
    data = {
        "code":0,
        "msg":"success",
        "count":len(us),
        "data":[u.to_dict() for u in us]
    }
    return jsonify(data)

