from forms import RegisterForm, Login, SearchBookForm, ChangePasswordForm, SearchUserForm, SearchCommentForm
from flask import Blueprint, render_template, request, url_for, session, redirect, jsonify, flash, g, make_response
from exts import db
from datetime import datetime
from models import *

def get_current_user():
    account_id = session.get('account_id')
    account = None
    if account_id:
        account = UserModel.query.filter_by(account_name=account_id).first()
    return account

admin = Blueprint('admin', __name__)

# go to admin page
@admin.route('/admin/index', methods=['GET', 'POST'])
def index():
    return render_template('base.html',account=get_current_user())

# get the user message
@admin.route('/admin/admin_info')
def admin_info():
    return render_template('admin-info.html',account=get_current_user())



# go to the page upload the book
@admin.route('/admin/upload_book')
def upload_book():
    return render_template('upload-book.html', account=get_current_user())

# add the user
@admin.route('/admin/adduser')
def adduser():
    return render_template('admin-adduser.html', account=get_current_user())
# add the admin
@admin.route('/admin/addadmin')
def addadmin():
    return render_template('admin-addadmin.html', account=get_current_user())

# update user
@admin.route('/admin/update_user')
def update_user():
    return render_template('admin-update_user.html', account=get_current_user())

# update the information of books
@admin.route('/admin/update_book')
def update_book():
    return render_template('admin-update_book.html', account=get_current_user())

# show the books in dashboard
@admin.route('/admin/book_list')
def book_list():
    books = BookModel.query.all()
    form = SearchBookForm()

    return render_template('admin-book-list.html', account=get_current_user(),books=books,form=form)
# user list
@admin.route('/admin/user_list')
def user_list():
    books = BookModel.query.all()
    form = SearchUserForm()

    return render_template('admin-user-list.html', account=get_current_user(),books=books,form=form)

# query of comment, find the suitable one
@admin.route('/admin/comments_query', methods=['GET', 'POST'])
def comments_query():
    query_content = request.args.get('content')
    query_method = request.args.get('method')
    print(f"query_content:{query_content},query_method:{query_method}")

    cms = CommentModel.query.all()
    data=[]
    for cm in cms:
        cm_id = cm.id
        book_id = cm.book_id
        user_id = cm.user_id
        content = cm.comment
        cm_time = cm.create_time

        # print(f"cm_id:{cm_id},book_id:{book_id},user_id:{user_id},content:{content},cm_time:{cm_time}")

        curbook = BookModel.query.filter_by(id=book_id).first()
        curuser = UserModel.query.filter_by(id=user_id).first()

        book_name = curbook.book_name
        user_name = curuser.username

        if query_content is not None and query_content.strip()!='':
            if query_method=='book_name':
                if query_content not in book_name:
                    continue
            elif query_method=='user_name':
                if query_content not in user_name:
                    continue
            elif query_method == 'content':
                if query_content not in content:
                    continue
            elif query_method == 'time':
                if query_content not in cm_time:
                    continue

        cur_dict={}
        cur_dict['cm_id']=cm_id
        cur_dict['book_name'] = book_name
        cur_dict['user_name'] = user_name
        cur_dict['content'] = content
        cur_dict['cm_time'] = cm_time
        data.append(cur_dict)
    res = {
        "code": 0,
        "msg": "",
        "count": len(data),
        "data": data
    }
    return res

# find all comments
@admin.route('/admin/comments_json')
def comments_json():
    cms = CommentModel.query.all()
    data=[]
    for cm in cms:
        cm_id = cm.id
        book_id = cm.book_id
        user_id = cm.user_id
        content = cm.comment
        cm_time = cm.create_time

        # print(f"cm_id:{cm_id},book_id:{book_id},user_id:{user_id},content:{content},cm_time:{cm_time}")

        curbook = BookModel.query.filter_by(id=book_id).first()
        curuser = UserModel.query.filter_by(id=user_id).first()

        book_name = curbook.book_name
        user_name = curuser.username

        cur_dict={}
        cur_dict['cm_id']=cm_id
        cur_dict['book_name'] = book_name
        cur_dict['user_name'] = user_name
        cur_dict['content'] = content
        cur_dict['cm_time'] = cm_time
        data.append(cur_dict)

    res = {
        "code":0,
        "msg":"",
        "count":len(data),
        "data":data
    }
    return res
# get the file
@admin.route('/admin/comments')
def comments():
    form = SearchCommentForm()
    return render_template('admin-comments-list.html', account=get_current_user(),form=form)

# delete the comments
@admin.route('/admin/delete_comment')
def delete_comment():
    comment_id = request.args.get('comment_id')
    print(f"commid:{comment_id}")
    delete_comment=CommentModel.query.filter_by(id=comment_id).first()
    if delete_comment is None:
        flash(u'The comment id is not exist')
        form = SearchCommentForm()
        return render_template('admin-comments-list.html', account=get_current_user(), form=form)
    db.session.delete(delete_comment)
    db.session.commit()
    flash(f'delete comment {comment_id} successfully')
    form = SearchCommentForm()
    return render_template('admin-comments-list.html', account=get_current_user(), form=form)