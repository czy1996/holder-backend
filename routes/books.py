from flask import (
    Blueprint,
    jsonify,
    request,
)
from utils import (
    json_response,
    log,
)
from models.book import Book

main = Blueprint('books', __name__)


@main.route('/all')
def books_all():
    bs = Book.all()
    return json_response([b.json() for b in bs])


@main.route('/<int:id>')
def book_id(id):
    b = Book.get(id)
    return json_response(b.json())


@main.route("/add", methods=["POST"])
def add():
    data = request.get_json()
    # log(data)
    b = Book.isbn(data["isbn"])
    return json_response(b.json())


@main.route('/delete/<int:id>')
def delete(id):
    b = Book.get(id)
    b.delete()
    return json_response(Book.get(id).json())


@main.route('/update/<int:id>', methods=['POST'])
def update(id):
    b = Book.get(id)
    data = request.json
    b.update(data)
    return json_response(Book.get(id).json())


@main.route('/get')
def get():
    r = {
        "status": "no",
    }
    title = request.args.get('title')
    books = Book.find(title=title)
    if books:
        r['status'] = 'ok'
        r['books'] = [b.json() for b in books]
    return json_response(r)
