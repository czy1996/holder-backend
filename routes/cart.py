from flask import (
    Blueprint,
    request,
    jsonify,
)
from models.user import User
from models.book import Book
from models.order import Order

from utils import log, json_response

import datetime

main = Blueprint('cart', __name__)


@main.route('/add/<int:id>')
def add_cart(id):
    """
    get code return session
    :return: 
    """
    u = User.current_user()
    b = Book.get(id)
    log('inventoty', b.inventory)
    if b.inventory < u.cart.get(str(id), 0) + 1:
        r = {
            'success': False
        }
    else:
        r = {
            'success': True
        }
        u.add_cart(id)
    return jsonify(r)


@main.route('/get')
def get_cart():
    log('headers', request.headers)
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


@main.route('/update', methods=['POST'])
def update_cart():
    u = User.current_user()
    data = request.json
    u.update_cart(data)
    return jsonify(u.json())


@main.route('/close')
def close_cart():
    u = User.current_user()
    cart = u.cart
    Book.dec(cart)
    o = Order.new(user=u.id, items=cart, orderType='购买')
    return jsonify(o.json())
