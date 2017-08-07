from flask import (
    Blueprint,
    request,
    jsonify,
)
from models.user import User
from models.book import Book

from utils import log, json_response

main = Blueprint('user', __name__)


@main.route('/addCart/<int:id>')
def add_cart(id):
    """
    get code return session
    :return: 
    """
    u = User.current_user()
    u.add_cart(id)
    return jsonify(u.json())


@main.route('/getCart')
def get_cart():
    u = User.current_user()
    log(u.cart.items())
    r = []
    for k, v in u.cart.items():
        b = Book.get(int(k)).json()
        b.update({
            'quantity': v,
        })
        r.append(b)
    # r = [Book.get(int(k)).json().update({'quantity': v}) for k, v in u.cart.items()]
    return json_response(r)


@main.route('/updateCart', methods=['POST'])
def update_cart():
    u = User.current_user()
    data = request.json
    u.update({
        'cart': data,
    })
    return jsonify(u.json())
