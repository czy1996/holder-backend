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

main = Blueprint('order', __name__)


@main.route('/get')
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
