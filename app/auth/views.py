from . import auth
from .. import dbdir
from flask import request
import sqlite3

@auth.route('/api/V1.0/user/register',methods=['POST'])
def api_register():
    args=request.get_json()
    

@auth.route('/api/V1.0/user/login',methods=['GET'])
def api_login():
    pass

@auth.route('/api/V1.0/user/set_info',methods=['POST'])
def api_set_info():
    pass

@auth.route('/api/V1.0/user/get_info',methods=['GET'])
def api_register():
    pass



