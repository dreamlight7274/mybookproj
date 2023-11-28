from forms import RegisterForm, Login, SearchBookForm
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

book = Blueprint('book', __name__)

# show selected the books
@book.route('/book/list_query', methods=['GET', 'POST'])
def list_query():
    content = request.args.get('content')
    method = request.args.get('method')

    print(f"content:{content},method:{method}")

    account_id = session.get('account_id')
    account = None
    if account_id:
        account = UserModel.query.filter_by(account_name=account_id).first()
    books = None
    if method=='book_name':
        books = BookModel.query.filter(BookModel.book_name.like('%'+content+'%')).all()
    elif method == 'author':
        books = BookModel.query.filter(BookModel.author.like('%'+content+'%')).all()
    elif method == 'isbn':
        books = BookModel.query.filter(BookModel.isbn.like('%'+content+'%')).all()
    elif method == 'intr':
        books = BookModel.query.filter(BookModel.intr.like('%'+content+'%')).all()
    # if you input nothing, maybe...... emmm, but, there is the solution,search all books
    if content.strip() =='':
        books = BookModel.query.all()
    data = {
        "code":0,
        "msg":"success",
        "count":len(books),
        "data":[b.to_dict() for b in books]
    }
    # dictionary
    return jsonify(data)

# the view to show all the book list
@book.route('/book/list', methods=['GET', 'POST'])
def list():
    if request.method == 'GET':
        account_id = session.get('account_id')
        account=None
        if account_id:
            account = UserModel.query.filter_by(account_name=account_id).first()
        books = BookModel.query.all()
        form = SearchBookForm()
        return render_template('book-list.html', books = books, account=account,form=form)
        # return render_template('book-list.html')

# show all the books
@book.route('/book/listjson', methods=['GET', 'POST'])
def bookjson():
    books = BookModel.query.all()
    data = {
        "code":0,
        "msg":"",
        "count":len(books),
        "data":[b.to_dict() for b in books]
    }

    return data

@book.route('/book/find_book', methods=['GET', 'POST'])
def find_book():
    books = BookModel.query.all()
    print(f"find books")

# return success
@book.route('/book/test', methods=['GET', 'POST'])
def test():
    print("is a test")
    return jsonify({'status': 'success'})

# first delete all the comment, then delete all the books
@book.route('/book/delete_book', methods=['GET', 'POST'])
def delete_book():
    book_id = request.form['book_id']
    delete_book = BookModel.query.filter_by(id=book_id).first()
    if delete_book is None:
        flash(u'The book id is none')
        return render_template('admin-update_book.html', account=get_current_user())
    del_cms = CommentModel.query.filter_by(book_id=book_id)
    for cm in del_cms:
        db.session.delete(cm)
        db.session.commit()
    print(f"delete_book:{delete_book.id}")
    db.session.delete(delete_book)
    db.session.commit()
    flash(f'delete book {delete_book.id} successfully')
    return render_template('admin-update_book.html', account=get_current_user())

# update the information of book
@book.route('/book/update_book', methods=['GET', 'POST'])
def update_book():
    book_id = request.form['book_id']
    isbn = request.form['isbn']
    book_name = request.form['book_name']
    author = request.form['author']
    intr = request.form['intr']

    upt_book = BookModel.query.filter_by(id=book_id).first()
    if upt_book is None:
        flash(u'The book is not exist')
        return render_template('admin-update_book.html', account=get_current_user())
    # use id to find the book, so id cna not be changed
    if book_id is not None and book_id.strip()!='':
        upt_book.id=book_id
    if isbn is not None and isbn.strip()!='':
        upt_book.isbn=isbn
    if book_name is not None and book_name.strip()!='':
        upt_book.book_name=book_name
    if author is not None and author.strip()!='':
        upt_book.author=author
    if intr is not None and intr.strip()!='':
        upt_book.intr=intr
    db.session.commit()
    flash(f'update book id {book_id} successfully')
    return render_template('admin-update_book.html', account=get_current_user())

# get the details of book
@book.route('/book/detail', methods=['GET', 'POST'])
def detail():
    account_id = session.get('account_id')
    account = None
    if account_id:
        account = UserModel.query.filter_by(account_name=account_id).first()
    book_id = request.args.get('id')
    book = BookModel.query.filter_by(id=book_id).first()
    coms = CommentModel.query.filter_by(book_id=book_id).order_by(CommentModel.create_time.desc()).all()
    res=[]
    # just a list, we need to transfer it to json in the template
    for com in coms:
        cur_json={}
        cur_user = UserModel.query.filter_by(id=com.user_id).first()
        print(f"cur_user:{cur_user},id:{com.user_id}",)
        cur_json['username']=cur_user.username
        cur_json['content']=com.comment
        cur_json['time']=com.create_time
        res.append(cur_json)
    print(f"size:{len(res)}")
    return render_template('book-detail.html', book=book, coms=res,account=account)
# get the message of books, and get the data of comment, at last get the data of comments

# add the account
@book.route('/book/add_comment', methods=['GET', 'POST'])
def add_comment():
    book_id = request.args.get('book_id')
    content = request.args.get('content')
    account_id = session.get('account_id')
    if account_id is None:
        print("return fails")
        return jsonify({'status': 'fail'})
    user = UserModel.query.filter_by(account_name=account_id).first()
    current_time = datetime.now()
    formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
    new_comment = CommentModel(book_id=book_id,user_id=user.id,comment=content,create_time=formatted_time,update_time=formatted_time)
    db.session.add(new_comment)
    db.session.commit()

    res={'success': True,'username':user.username,'content':content,'time':formatted_time}
    return jsonify(res)

# uploading the picture
@book.route('/book/uploading', methods=['GET', 'POST'])
def uploading():
    print("trigger uploading")
    file = request.files['file']
    fname= str(file.filename)
    if file and ('jpg' in fname or 'JPG' in fname or 'PNG' in fname or 'png' in fname):
        file.save(f'./static/images/{file.filename}')
        return {'code': 0, 'status': 'success', 'pic': file.filename}
    return {'code': 500,'status': 'fail'}

# add new book
@book.route('/book/add_newbook', methods=['GET', 'POST'])
def add_newbook():
    if request.method == 'POST':
        # get the message
        book_name = request.form['book_name']
        isbn = request.form['isbn']
        author = request.form['author']
        introduction = request.form['introduction']

        pic_name = request.form['pic_name']

        print(f'book_name:{book_name},isbn:{isbn},author:{author},introduction:{introduction},pic_name:{pic_name}')
        bm = BookModel()
        bm.isbn=isbn
        bm.book_name=book_name
        bm.image=pic_name
        bm.author=author
        bm.intr=introduction

        now = datetime.now()
        formatted_time = str(now.strftime("%Y-%m-%d %H:%M:%S"))

        bm.create_time=bm.update_time=formatted_time
        db.session.add(bm)
        db.session.commit()
        flash(f'add a new book successfully')

        return render_template('upload-book.html', account=get_current_user())