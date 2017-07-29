from flask import (
    Flask,
    Blueprint,
)
from flask_wxapp import WXApp

from config import app_id, secret

from routes.login import main as login_routes
from routes.books import main as books_routes

wxapp = WXApp()


def create_app():
    app = Flask(__name__)
    app.config.update(WX_APPID=app_id,
                      WX_SECRET=secret)
    wxapp.init_app(app)

    app.register_blueprint(login_routes, url_prefix='/login')
    app.register_blueprint(books_routes, url_prefix='/book')

    return app


app = create_app()


@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    config = dict(
        debug=True,
        host='0.0.0.0',
        port=5000,
    )
    app.run(**config)
