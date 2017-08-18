from flask import (
    Blueprint,
    request,
    jsonify,
)
from models.user import User
from models.book import Book
from models.order import Order

from utils import log, json_response

main = Blueprint('sell', __name__)


@main.route('/add/<int:id>')
def add_sells(id):
    """
    get code return session
    :return: 
    """
    u = User.current_user()
    u.add_sells(id)
    return jsonify(u.json())


@main.route('/get')
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


@main.route('/update', methods=['POST'])
def update_sells():
    u = User.current_user()
    data = request.json
    u.update_sells(data)
    return jsonify(u.json())


@main.route('/close')
def close_sells():
    u = User.current_user()
    sells = u.sells
    o = Order.new(user=u.id, items=sells, orderType='卖出')
    return jsonify(o.json())
