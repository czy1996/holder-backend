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


@main.route('/getInfo')
def get_info():
    u = User.current_user()
    r = {
        'is_info': u.is_info,
        'name': u.name,
        'phone': u.phone,
        'dorm': u.dorm
    }
    return json_response(r)


@main.route('/updateInfo', methods=['POST'])
def update_info():
    u = User.current_user()
    data = request.json
    up = {
        'is_info': True
    }
    up.update(data)
    u.update(up)
    return json_response(u.json())
