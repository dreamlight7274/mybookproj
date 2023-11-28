from flask import Blueprint, render_template, request, url_for, session
from models import *

def get_current_user():
    account_id = session.get('account_id')
    account = None
    if account_id:
        account = UserModel.query.filter_by(account_name=account_id).first()
    return account