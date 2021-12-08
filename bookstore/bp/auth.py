from flask import Blueprint
from flask import request
from flask import jsonify
from be.model.auth import *
import random


bp = Blueprint('auth', __name__, url_prefix = "/auth")


@bp.route('/register', methods = ['POST'])
def register():
    params = request.json
    user_id = params["user_id"]
    password = params["password"]
    user = User()
    if user.register(user_id, password):
        code = 200
        body = {"message": "OK"}
    else:
        code = 500
        body = {"message": "用户名重复，注册失败！"}
    return jsonify(body), code


@bp.route('/unregister', methods = ['POST'])
def unregister():
    params = request.json
    user_id = params["user_id"]
    password = params["password"]
    user = User()
    if user.unregister(user_id, password):
        code = 200
        body = {"message": "OK"}
    else:
        code = 401
        body = {"message": "注销失败，用户名不存在或密码不正确"}
    return jsonify(body), code


@bp.route('/login', methods = ['POST', 'GET'])
def login():
    params = request.json
    user_id = params["user_id"]
    password = params["password"]
    terminal = ''.join(str(random.choice(range(10))) for _ in range(10))
    user = User()
    token = user.login(user_id, password, terminal)
    if token is not None:
        code = 200
        body = {"message": "OK", "token": token}
    else:
        code = 401
        body = {"message": "登录失败，用户名或密码错误"}
    return jsonify(body), code


@bp.route("/password", methods=["POST"])
def password():
    params = request.json
    user_id = params["user_id"]
    old_password = params["oldPassword"]
    new_password = params["newPassword"]
    user = User()
    if user.password(user_id, old_password, new_password):
        code = 200
        body = {"message": "OK"}
    else:
        code = 401
        body = {"message": "更改密码失败"}
    return jsonify(body), code


@bp.route('/logout', methods = ['POST'])
def logout():
    params = request.json
    user_id = params["user_id"]
    token = request.headers["token"]
    user = User()
    if user.logout(user_id, token):
        code = 200
        body = {"message": "登出成功"}
    else:
        code = 401
        body = {"message": "登出失败，用户名或token错误"}
    return jsonify(body), code
