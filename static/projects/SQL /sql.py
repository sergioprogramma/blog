import sqlite3
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, request, redirect, url_for
# from typing import Callable
#
#
# class MySQLAlchemy(SQLAlchemy):  # Or you can add the below code on the SQLAlchemy directly if you think to modify the package code is acceptable.
#     Column: Callable  # Use the typing to tell the IDE what the type is.
#     String: Callable
#     Integer: Callable
# # db.create_all()
#
# db = sqlite3.connect("books-collection.db")
# cursor = db.cursor()
# cursor.execute("CREATE TABLE element (id INTEGER PRIMARY KEY, title varchar(250) NOT NULL UNIQUE, author varchar(250) NOT NULL, rating FLOAT NOT NULL)")
#
# cursor.execute("INSERT INTO books VALUES(1, 'Harry Potter', 'J. K. Rowling', '9.3')")
# db.commit()


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books-collection.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    author = db.Column(db.String(250), nullable=False)
    rating = db.Column(db.Float, nullable=False)

    # def __repr__(self):
    #     return f'<Book {self.name}>'

#
# db.create_all()
# book_id = 1
# book_to_delete = Book.query.get(book_id)
# db.session.delete(book_to_delete)
# db.session.commit()
#
# book_id = 5
# book_to_delete = Book.query.get(book_id)
# db.session.delete(book_to_delete)
# db.session.commit()

# CREATE RECORD
# new_book = Book(id=1, name="Harry", author="J. K. Rowling", rating=9.3)
# db.session.add(new_book)
# db.session.commit()
#
# new_book = Book(id=2, name="Angela", author="J. K. Rowling", rating=95)
# db.session.add(new_book)
# db.session.commit()
#
# all_books = db.session.query(Book).all()
# book = Book.query.filter_by(name="Harry").first()
# print(book)

# Update A Record By PRIMARY KEY
book_id = 2
book_to_update = Book.query.get(book_id)
book_to_update.name = "Harry Potter and belli "
db.session.commit()

# book_id = 2
# book_to_delete = Book.query.get(book_id)
# db.session.delete(book_to_delete)
# db.session.commit()

# book_id = request.form["id"]
# book_to_update = Book.query.get(book_id)
# book_to_update.rating = request.form["rating"]
# db.session.commit()