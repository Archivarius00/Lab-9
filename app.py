from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(200), nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Book {self.name} by {self.author}>'

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        book_author = request.form['author']
        book_name = request.form['name']
        
        new_book = Book(author=book_author, name=book_name)
        
        try:
            db.session.add(new_book)
            db.session.commit()
            return redirect('/')
        except:
            return 'При добавлении книги произошла ошибка'
    else:
        books = Book.query.order_by(Book.date_added).all()
        return render_template('index.html', books=books)

@app.route('/clear', methods=['POST'])
def clear():
    try:
        db.session.query(Book).delete()
        db.session.commit()
        return redirect('/')
    except:
        return 'При очистке списка произошла ошибка'

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)