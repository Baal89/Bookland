import os
from flask import (
    Flask, render_template,
    flash, session, redirect, request, url_for)
from flask_pymongo import PyMongo
import json
from bson.objectid import ObjectId
from bson import json_util
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
if os.path.exists("env.py"):
    import env

app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'Bookland'
app.config['MONGO_URI'] = os.environ.get('MONGO_URI')
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')

mongo = PyMongo(app)


@app.route('/')
def index():
    return render_template('index.html',
                           books=mongo.db.books.find(),
                           page_title='index')


@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        existing_user = mongo.db.users.find_one(
            {'username': request.form.get('username').lower()})

        if existing_user:
            flash('Username already exists')
            return redirect(url_for('register'))

        register = {
            "username": request.form.get("username").lower(),
            "email": request.form.get("email"),
            "password": generate_password_hash(request.form.get("password")),
            }

        mongo.db.users.insert_one(register)
        session["user"] = request.form.get("username").lower()
        flash("Registration Succesfull!")
        return redirect(url_for('profile', username=session['user']))
    return render_template('register.html')


@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        existing_user = mongo.db.users.find_one(
            {'username': request.form.get('username').lower()})

        if existing_user:
            if check_password_hash(existing_user['password'], request.form.get('password')):
                session['user'] = request.form.get('username').lower()
                flash("Welcome,{}".format(request.form.get('username')))
                return redirect(url_for('profile', username=session['user']))
            else:
                flash('Incorrect Username and/or Password')
                return redirect(url_for('login'))

        else:
            flash('Incorrect Username and/or Password')
            return redirect(url_for('login'))
    return render_template("login.html")


@app.route('/profile', methods=['POST', 'GET'])
def profile():
    username = mongo.db.users.find_one(
        {'username': session['user']})['username']
    reviews = mongo.db.reviews.find({'user': session['user']})

    if session['user']:
        return render_template('profile.html', username=username, reviews=reviews)

    return redirect(url_for('login'))


@app.route('/logout')
def logout():
    flash('You have been logged out')
    session.pop('user')
    return redirect(url_for('index'))


@app.route('/get_book/<book_id>')
def get_book(book_id):
    reviews = mongo.db.reviews.find({'id': ObjectId(book_id)})
    a_book = mongo.db.books.find_one({'_id': ObjectId(book_id)})
    return render_template('getbook.html', book=a_book, reviews=reviews)


@app.route('/add_book')
def add_book():
    return render_template('addbook.html')


@app.route('/insert_book', methods=['POST'])
def insert_book():
    books = mongo.db.books
    books.insert_one(request.form.to_dict())
    flash('The book has been added!')
    return redirect(url_for('index'))


@app.route('/edit_book/<book_id>')
def edit_book(book_id):
    a_book = mongo.db.books.find_one({'_id': ObjectId(book_id)})
    return render_template('editbook.html', book=a_book)


@app.route('/update_book/<book_id>', methods=['POST'])
def update_book(book_id):
    books = mongo.db.books
    books.update({'_id': ObjectId(book_id)},

    {
        'book_title': request.form.get('book_title'),
        'category_name': request.form.get('category_name'),
        'book_author': request.form.get('book_author'),
        'book_image': request.form.get('book_image'),
        'collection_name': request.form.get('collection_name'),
        'book_description': request.form.get('book_description')
    })

    flash("The book has been updated")
    return redirect(url_for('index'))


@app.route('/add_review/<book_id>')
def add_review(book_id):
    a_book = mongo.db.books.find_one({'_id': ObjectId(book_id)})
    return render_template('addreview.html', book=a_book)


@app.route('/insert_review/<book_id>', methods=['POST'])
def insert_review(book_id):
    book_id = ObjectId(book_id)
    username = mongo.db.users.find_one(
        {'username': session['user']})['username']
    rating = float(request.form.get('review_rating'))

    submission = {
        'id': book_id,
        'user': username,
        'book_title': request.form.get('book_title'),
        'review_title': request.form.get('review_title'),
        'review_rating': rating,
        'review_description': request.form.get('review_description'),
        'date': datetime.utcnow(),
    }

    reviews = mongo.db.reviews
    reviews.insert_one(submission)
    flash('Your review has been added!')
    return redirect(url_for('get_book', book_id=book_id, username=username))


@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')


@app.route('/data')
def data():
    FIELDS = {'_id': False, 'book_title': True, 'review_rating': True}

    projects = mongo.db.reviews.find({}, FIELDS)
    json_projects = []
    for project in projects:
        json_projects.append(project)
    json_projects = json.dumps(json_projects, default=json_util.default)
    return json_projects


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)
