from flask import Flask
from flask import request
from bookstore.bp import auth, buyer, seller, extra
import waitress

from bookstore.bp.extra import search 

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World'

@app.route('/shutdown')
def shutdown():
    return be_shutdown()

def run_server(debug=False):
    app.register_blueprint(auth.bp)
    app.register_blueprint(buyer.bp)
    app.register_blueprint(seller.bp)
    app.register_blueprint(extra.bp)
    app.run(debug = debug, threaded=True)


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
