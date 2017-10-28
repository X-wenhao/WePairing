from functools import wraps
from flask import session,jsonify
import hashlib

class HttpAuth(object):
    '''
    用户认证相关
    '''
    def login_required(self,f):
        @wraps(f)
        def decorated(*args, **kwargs):
            if session.get('mail'):
                return f(*args, **kwargs)
            else:
                return jsonify({"result":"login error"})
        return decorated

    def login_user(self,mail):
        session['mail']=mail

    def hash_password(self,password):
        return hashlib.sha256(password.encode('utf-8'))


