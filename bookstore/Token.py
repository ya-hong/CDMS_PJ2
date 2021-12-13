from contextlib import ContextDecorator
import time
from hashlib import sha256

tokens = dict()


def decode(s):
    [t, code] = s.split('-')
    return int(t)


def encode(t, user_id, password, terminal):
    t = int(time.time())
    s = "{}-{}-{}".format(user_id, password, terminal)
    s = "{}-{}".format(t, sha256(s))
    return s


def clear():
    items = tokens.items()
    for key, value in items:
        for token in value[:]:
            t = decode(token)
            if time.time() - t > 60:
                value.remove(token)
            else:
                break
        if len(value) == 0:
            del tokens[key]


def check_token(user_id, token):
    clear()
    if user_id in tokens and token in tokens[user_id]:
        return True
    else:
        return False


def add_token(user_id, password, terminal):
    clear()
    code = encode(time.time(), user_id, password, terminal)
    print("生成token", code)
    if not user_id in tokens:
        tokens[user_id] = []
    tokens[user_id].append(code)
    return code
