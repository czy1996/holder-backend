from flask import (
    Blueprint,
    request,
    jsonify,
)
from models.user import User
from utils import log

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
