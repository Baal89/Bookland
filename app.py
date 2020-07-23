import os
import env
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId


app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'Bookland'
app.config['MONGO_URI'] = os.environ.get('MONGO_URI')

mongo = PyMongo(app)


@app.route('/')
def index():
    return render_template('index.html',
                           books=mongo.db.books.find(),
                           page_title='index')


@app.route('/get_book/<book_id>')
def get_book(book_id):
    a_book = mongo.db.books.find_one({'_id': ObjectId(book_id)})
    return render_template('getbook.html', book=a_book)


@app.route('/add_book')
def add_book():
    return render_template(
        'addbook.html',
        categories=mongo.db.categories.find())


@app.route('/insert_book', methods=['POST'])
def insert_book():

    rating = float(request.form.get('book_rating'))

    submission = {
        'book_title': request.form.get('book_title'),
        'category_name': request.form.get('category_name'),
        'book_author': request.form.get('book_author'),
        'book_image': request.form.get('book_image'),
        'collection_name': request.form.get('collection_name'),
        'book_rating': rating,
        'book_description': request.form.get('book_description')
    }

    books = mongo.db.books
    books.insert_one(submission)
    return redirect(url_for('index'))


@app.route('/edit_book/<book_id>')
def edit_book(book_id):
    a_book = mongo.db.books.find_one({'_id': ObjectId(book_id)})
    category = mongo.db.categories.find()
    return render_template('editbook.html', book=a_book, categories=category)


@app.route('/update_book/<book_id>', methods=['POST'])
def update_book(book_id):
    books = mongo.db.books
    books.update({'_id': ObjectId(book_id)}, {
        'book_title': request.form.get('book_title'),
        'category_name': request.form.get('category_name'),
        'book_author': request.form.get('book_author'),
        'book_image': request.form.get('book_image'),
        'collection_name': request.form.get('collection_name'),
        'book_rating': request.form.get('book_rating'),
        'book_description': request.form.get('book_description')
    })
    return redirect(url_for('index'))


@app.route('/delete_book/<book_id>')
def delete_book(book_id):
    mongo.db.books.remove({'_id': ObjectId(book_id)})
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)
