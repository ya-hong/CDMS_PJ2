from flask import Blueprint
from flask import request
from flask import jsonify
from flask import session
from bookstore.classes.model import *
from bookstore import error
from bookstore import Token
import random


bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/register', methods=['POST'])
def register():
    params = request.json
    user_id = params['user_id']
    password = params['password']

    try:
        User.create(user_id, password)
    except error.Err as err:
        # print(err)
        return err.ret()

    return error.ok.ret()


@bp.route('/unregister', methods=['POST'])
def unregister():
    params = request.json
    user_id = params['user_id']
    password = params['password']

    try:
        user = User(user_id)
        user.unregister(password)
    except error.NO_USER:
        return error.NO_PERMISSION({'message': '用户名不存在'}).ret()
    except error.Err as err:
        return err.ret()
    return error.ok.ret()


@bp.route('/login', methods=['POST'])
def login():
    params = request.json
    user_id = params['user_id']
    password = params['password']
    terminal = params['terminal']
    # token = None
    try:
        user = User(user_id)
        user.login(password, terminal)
        token = Token.add_token(user_id, password, terminal)
    except error.NO_USER:
        return error.NO_PERMISSION({'message': '用户名不存在'}).ret()
    except error.Err as err:
        return err.ret()
    return error.OK({'message': 'OK', 'token': token}).ret()


@bp.route("/password", methods=["POST"])
def password():
    params = request.json
    user_id = params["user_id"]
    old_password = params["oldPassword"]
    new_password = params["newPassword"]

    try:
        user = User(user_id)
        user.password(old_password, new_password)
    except error.NO_USER:
        return error.NO_PERMISSION({'message': '用户名不存在'}).ret()
    except error.Err as err:
        return err.ret()
    return error.ok.ret()


@bp.route('/logout', methods=['POST'])
def logout():
    params = request.json
    user_id = params["user_id"]
    token = request.headers.get("token")
    if not Token.check_token(user_id, token):
        return error.NO_PERMISSION({'message': 'token错误'}).ret()
    try:
        user = User(user_id)
        user.logout()
    except error.NO_USER:
        return error.NO_PERMISSION({'message': '用户名错误'}).ret()
    return error.ok.ret()
