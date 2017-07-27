from flask import (
    Blueprint,
    request,
    jsonify,
)
from models.user import User
from utils import log

main = Blueprint('login', __name__)


@main.route('/')
def login():
    """
    get code return session
    :return: 
    """
    code = request.args.get('code')
    session = User.auth(code)
    response = {
        'session_id': session
    }
    return jsonify(**response)
