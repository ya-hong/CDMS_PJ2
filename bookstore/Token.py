import time 

tokens = []


def decode(s):
    [t, user_id, password] = s.split('-')
    return int(t), user_id, password


def encode(t, user_id, password):
    t = int(time.time())
    s = "{}-{}-{}".format(t, user_id, password)
    return s


def clear():
    for token in tokens:
        t, user_id, password = decode(token)
        if time.time() - t > 60:
            tokens.remove(token)
        else:
            break


def check_token(token):
    clear()
    if token in tokens:
        return True
    else:
        return False


def add_token(user_id, password):
    clear()
    tokens.append(time.time(), user_id, password)

