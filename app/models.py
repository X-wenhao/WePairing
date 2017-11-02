from functools import wraps
from flask import session,jsonify
import hashlib
import sqlite3
from . import dbdir
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
        db=sqlite3.connect(dbdir)
        name=db.execute('select name from users where mail='+mail).fetchone()
        session['name']=name
        db.close()

    def hash_password(self,password):
        return hashlib.sha256(password.encode('utf-8'))


