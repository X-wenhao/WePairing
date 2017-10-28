from . import pair
from .. import dbdir,mail,httpauth
from flask import request,jsonify,current_app,session
from flask_mail import Message
import sqlite3
import time

quick_pairs_pool={}
divided_pairs_pool={}

@pair.route('/api/V1.0/quick_pairs/release_pair',methods=['POST'])
def api_release_pair():
    name=request.args.get('name')
    if not name:
        return jsonify({'result':0})
    args = request.get_json()
    keys=['location']
    if list(args.keys()) != keys:
        return jsonify({'result': 0})

    pair=dict(args)
    pair['time'] = time.strftime("%Y-%m-%d %X")
    pair['name']=name
    pair['result']=[]

    if pair['location'] not in divided_pairs_pool.keys():
        divided_pairs_pool['location']=[]
    if name not in divided_pairs_pool:
        divided_pairs_pool['location'].append(name)
    quick_pairs_pool[name]=pair
    return jsonify({'result':1})

@pair.route('/api/V1.0/quick_pairs/get_users',methods=['GET'])
def api_get_users():
    name = request.args.get('name')
    if not name or quick_pairs_pool.get(name) is None\
            or quick_pairs_pool['name'].get('result') == []:
        return jsonify({'result': 0})
    if len(quick_pairs_pool[name]['result']) <4:
        return jsonify({'result': 0})
    print(name+"request quick_pair result")

    keys = ['name', 'school', 'grade', 'major', 'gender', 'good_at', 'description', 'connection']
    db = sqlite3.connect(dbdir)
    re=[]
    for i in quick_pairs_pool[name].get('result'):
        sql = 'select name,school,grade,major,gender,good_at,description,connection from users where name=' + i
        values = list(db.execute(sql).fetchone())
        re.append(dict(zip(keys, values)))
    db.close()
    print(re)
    return jsonify(re)

def asnyc_pairing():
    while(True):
        for loc,name_list in divided_pairs_pool.items():
            if len(name_list)<4:
                continue
            for name in name_list[:4]:
                quick_pairs_pool[name]['result']=name_list[:4]
            divided_pairs_pool[loc]=name_list[4:]
        time.sleep(5)

@pair.route('/api/V1.0/quick_pairs/send_result',methods=['POST'])
def api_send_result():
    name = request.args.get('name')
    if not name:
        return jsonify({'result': 0})

    result = request.args.get('result')
    if not result:
        return jsonify({'result': 0})

    if int(result)==1:
        quick_pairs_pool.pop(name)
    else:
        divided_pairs_pool[quick_pairs_pool[name]['location']].append(name)

    db = sqlite3.connect(dbdir)
    sql = 'insert into quick_pairs(name,time,status)' \
          'values("{}","{}","{}")'.format(pair['name'],
                                          pair['time'],
                                          pair['status'])
    try:
        db.execute(sql)
    except:
        pass
    db.close()

    return jsonify({'result':1})

@pair.route('/api/V1.0/pairs/release_pair',methods=['POST'])
def api_release_pair():
    name = request.args.get('name')
    if not name:
        return jsonify({'result': 0})
    args = request.get_json()
    keys = ['type', 'title', 'description']
    if list(args.keys()) != keys:
        return jsonify({'result': 0})
    db=sqlite3.connect(dbdir)
    sql='insert into pairs(name,type,title,description)values("{}",""{}","{}","{}")'\
        .format(name,args['type'],args['title'],args['description'])
    db.execute(sql)
    db.close()
    return jsonify({'result': 1})

@pair.route('/api/V1.0/pairs/get_pairs',methods=['GET'])
def api_get_pairs():
    sql='select id, name,type,title from pairs'
    type=request.args.get('type')
    if not type:
        sql=sql+' where type='+type
    db=sqlite3.connect(dbdir)
    data=db.execute(sql).fetchall()
    re=[]
    keys=['id','name','type','title']
    for row in data:
        re.append(dict(zip(keys,list(row))))
    return jsonify(re)

@pair.route('/api/V1.0/pairs/get_pair',methods=['GET'])
def api_get_pair():
    id=request.args.get('id')
    if not id:
        return {'result':0}
    sql='select id,type,title,description,name,agreed_persons from pairs where id='+id
    db=sqlite3.connect(dbdir)
    data=list(db.execute(sql).fetchone())
    keys=['id','type','title','description','name']
    re=dict(zip(keys,data[:-1]))
    re['people_num']=len(data[-1].split())
    return jsonify(re)


