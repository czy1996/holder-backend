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
    u.update_cart(data)
    return jsonify(u.json())


@main.route('/closeCart')
def close_cart():
    u = User.current_user()
    cart = u.cart
    o = Order.new(user=u.id, items=cart, orderType='购买')
    return jsonify(o.json())


@main.route('/getOrders')
def get_orders():
    u = User.current_user()
    l = Order.find(user=u.id)
    l = [o.json() for o in l]
    l.reverse()
    for order in l:
        r = []
        for id, q in order['items'].items():
            log(id, q)
            title = Book.get(int(id)).title
            r.append({
                'title': title,
                'quantity': q,
            })
        order['items'] = r
        order['time'] = datetime.datetime.fromtimestamp(order['ct']).strftime("%Y-%m-%d %H:%M:%S")
    return json_response(l)


@main.route('/addSells/<int:id>')
def add_sells(id):
    """
    get code return session
    :return: 
    """
    u = User.current_user()
    u.add_sells(id)
    return jsonify(u.json())


@main.route('/getSells')
def get_sells():
    u = User.current_user()
    log(u.sells.items())
    r = []
    for k, v in u.sells.items():
        b = Book.get(int(k)).json()
        b.update({
            'quantity': v,
        })
        r.append(b)
    # r = [Book.get(int(k)).json().update({'quantity': v}) for k, v in u.cart.items()]
    return json_response(r)


@main.route('/updateSells', methods=['POST'])
def update_sells():
    u = User.current_user()
    data = request.json
    u.update_sells(data)
    return jsonify(u.json())


@main.route('/closeSells')
def close_sells():
    u = User.current_user()
    sells = u.sells
    o = Order.new(user=u.id, items=sells, orderType='卖出')
    return jsonify(o.json())
