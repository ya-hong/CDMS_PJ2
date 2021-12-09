# auth接口

from flask import Blueprint
from flask import Flask
from flask import request

# auth = Blueprint("auth", __name__)

auth = Flask(__name__)
auth.run(processes=True)


@auth.route("/auth/register", methods=["POST"])
def register():
    params = request.json
    user_id = params["user_id"]
    password = params["password"]
    return
