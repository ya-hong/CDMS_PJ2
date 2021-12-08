from flask import Blueprint
from flask import request


bp = Blueprint('auth', __name__, url_prefix = "/auth")


@bp.route('/register', methods = ['POST'])
def register():
    return 


@bp.route('/unregister', methods = ['POST'])
def unregister():
    return 


@bp.route('/login', methods = ['POST', 'GET'])
def login():
    print('login')
    return 'hello', 200


@bp.route('/logout', methods = ['POST'])
def logout():
    return