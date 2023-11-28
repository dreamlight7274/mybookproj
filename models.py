from exts import db
from datetime import datetime

# user table
class UserModel(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(100), nullable=False)
    account_name = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    create_time = db.Column(db.String(200))
    update_time = db.Column(db.String(200))
    auth_type = db.Column(db.Integer, default=2) # 1 for admin, 2 for user

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'account_name': self.account_name,
            'create_time': self.create_time,
            'update_time': self.update_time,
            'auth_type': self.auth_type
        }


# book table
class BookModel(db.Model):
    __tablename__ = 'book'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    isbn = db.Column(db.String(20), nullable=False)
    book_name = db.Column(db.String(100), nullable=False)
    image = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=True)
    intr = db.Column(db.String(500), nullable=True)
    create_time = db.Column(db.String(200))
    update_time = db.Column(db.String(200))
    def to_dict(self):
        return {
            'id': self.id,
            'isbn': self.isbn,
            'book_name': self.book_name,
            'image_path': self.image,
            'author': self.author,
            'intr': self.intr,
            'create_time': self.create_time,
            'update_time': self.update_time
        }

class CommentModel(db.Model):
    __tablename__ = 'comment'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    book_id = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.String(500), nullable=True)
    create_time = db.Column(db.String(200))
    update_time = db.Column(db.String(200))

    def __init__(self, book_id,user_id,comment,create_time,update_time):
        self.book_id = book_id
        self.user_id = user_id
        self.comment = comment
        self.create_time = create_time
        self.update_time = update_time


