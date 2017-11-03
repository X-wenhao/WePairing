from . import auth
from .. import dbdir,mail,httpauth
from flask import request,jsonify,current_app,session
from flask_mail import Message
import sqlite3
import random


@auth.route('/api/V1.0/user/register',methods=['POST'])
def api_register():
    args=request.get_json()
    if list(args.keys()) != ['mail','vertification_code','password']:
        return jsonify({'result':0})
    if session.get(args.get['ver_code']) is None or \
                    session.get(args['ver_code'])!=args['vertification_code']:
        return jsonify({'result':0})

    db=sqlite3.connect(dbdir)

    sql='select mail from users where mail={}'.format(args['mail'])
    if db.execute(sql).fetchone():
        db.close()
        return jsonify({'result':0})
    hashed_pwd=httpauth.hash_password(args['password'])

    sql='insert into users(mail,password)values({},{})'.format(args['mail'],hashed_pwd)
    db.execute(sql)
    db.close()

    return jsonify({'result':1})


@auth.route('/api/V1.0/user/send_mail',methods=['POST'])
def api_send_mail():
    print('mail...')
    args_dict = {}
    # args_dict['address']=request.args.get('address')
    # args_dict['content']=request.args.get('content')
    args_dict = request.get_json()
    print(args_dict)
    msg = Message("验证码", sender=current_app.config['MAIL_USERNAME'], recipients=[args_dict.get('mail')])
    # print(args_dict['address'])
    # print(args_dict['content'])

    ver_code=random.randint(100000,999999)
    session[args_dict['ver_code']]=ver_code
    msg.body =ver_code

    try:
        mail.send(msg)
    except:
        session.pop(args_dict['mail'])
        return jsonify({'result': 0})

    return jsonify({'result': 1})

@auth.route('/api/V1.0/user/login',methods=['GET'])
def api_login():
    args = request.get_json()
    if list(args.keys()) != ['mail', 'password']:
        return jsonify({'result': 0})

    sql='select password from users where mail={}'.format(args['mail'])
    db=sqlite3.connect(dbdir)
    hashed_pwd=db.execute(sql).fetchone()

    if not hashed_pwd:
        return jsonify({'result':0})
    if not hashed_pwd==httpauth.hash_password(args['password']):
        return jsonify({'result': 0})

    httpauth.login_user(args['mail'])
    db.close()

    return jsonify({'result': 1})


@auth.route('/api/V1.0/user/set_info',methods=['POST'])
def api_set_info():
    mail=request.args.get('mail')
    if session.get('mail') != mail:
        return jsonify({"result":0})

    args = dict(request.form)
    keys=['name','school','grade','major','gender','good_at','description','connection','icon_url']
    if list(args.keys()) != keys[:-1]:
        return jsonify({'result': 0})
    sql='update users set'
    db=sqlite3.connect(dbdir)
    for key in keys[:-1]:
        sql+=' {}={},'.format(key,args[key])
    sql=sql[:-1]
    sql+=' where mail='+mail
    db = sqlite3.connect(dbdir)
    db.execute(sql)
    db.close()
    session['name']=args['name']
    return jsonify({'result':1})


@auth.route('/api/V1.0/user/get_info',methods=['GET'])
def api_get_info():
    name=request.args.get('name')
    if not name:
        return jsonify({'result':0})
    args = request.get_json()
    keys = ['name', 'school', 'grade', 'major', 'gender', 'good_at', 'description', 'connection','icon_url']
    if list(args.keys()) != keys:
        return jsonify({'result': 0})
    sql='select name,school,grade,major,gender,good_at,description,connection from users where name='+name
    db=sqlite3.connect(dbdir)
    values=list(db.execute(sql).fetchone())
    re=dict(zip(keys,values))
    db.close()
    return jsonify(re)


