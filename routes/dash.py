from flask import (
    Blueprint,
    jsonify,
    request,
    render_template,
)
from utils import (
    json_response,
    log,
)
from models.book import Book

main = Blueprint('dash', __name__)


@main.route('/')
def index():
    return render_template('dashboard/index.html')
