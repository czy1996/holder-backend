from flask import (
    Blueprint,
    jsonify,
)
import json
from utils import json_response
from models.book import Book

main = Blueprint('books', __name__)


@main.route('/all')
def books_all():
    bs = Book.all()
    return json_response([b.json() for b in bs])
