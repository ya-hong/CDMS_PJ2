import os
import sys
sys.path.append('./')

from flask import Flask
from flask import request
from flask import session
import bp


app = Flask(__name__)
app.config["SECRET_KEY"] = os.urandom()


@app.route('/')
def hello_world():
    return 'Hello World'


def run_server(debug=False):
    app.register_blueprint(bp.auth.bp)
    app.register_blueprint(bp.buyer.bp)
    app.register_blueprint(bp.seller.bp)
    app.run(debug=debug)


def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()


def be_run():
    run_server()
    return "Server start"


def be_shutdown():
    shutdown_server()
    return "Server shutting down..."


if __name__ == '__main__':
    run_server(debug=True)
