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
    data = request.get_json(force=True)
    log(data)
    b = Book.new(data)
    return json_response(b.json())
