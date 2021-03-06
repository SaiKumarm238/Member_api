from flask import Flask, request, g, jsonify
from flask_cors import CORS, cross_origin
from database import get_db
from functools import wraps

app = Flask(__name__)
CORS(app)

api_username = 'admin'
api_password = '10031'

def protected(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if auth and auth.username == api_username and auth.password == api_password:
            return f(*args, **kwargs)
    
        return jsonify({'message':'Autentication failed!'}), 403
    return decorated

@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()

@app.route('/member', methods=['GET'])
@cross_origin()
@protected
def get_members():
    db = get_db()
    members_cur = db.execute('select id, name, email, level from members')
    members = members_cur.fetchall()

    return_values = []

    for member in members:
        member_dict = {}
        member_dict['id'] = member['id']
        member_dict['name'] = member['name']
        member_dict['email'] = member['email']
        member_dict['level'] = member['level']

        return_values.append(member_dict)

    return jsonify({'members': return_values})

@app.route('/member/<int:member_id>', methods=['GET'])
@cross_origin()
@protected
def get_member(member_id):

    db = get_db()

    member_cur = db.execute('select id, name,email,level from members where id= ?',[member_id])
    member = member_cur.fetchone()

    member_dict = {}
    member_dict['id']= member['id']
    member_dict['name']= member['name']
    member_dict['email']= member['email']
    member_dict['level']= member['level']

    return jsonify({"member": member_dict})

@app.route('/member', methods=['POST'])
@cross_origin()
@protected
def add_member():

    db = get_db()

    new_member_date = request.get_json()

    name = new_member_date['name']
    email = new_member_date['email']
    level = new_member_date['level']

    db.execute('insert into members (name, email, level) values (?,?,?)',[name,email,level])
    db.commit()

    member_cur = db.execute('select id, name,email,level from members where name= ?',[name])
    new_member = member_cur.fetchone()

    return jsonify({"members" : {'id' : str(new_member['id']), 'name': new_member['name'], 'email': new_member['email'], 'level': new_member['level']}})

@app.route('/member/<int:member_id>', methods=['PUT','PATCH'])
@cross_origin()
@protected
def edit_member(member_id):

    db = get_db()

    new_member_date = request.get_json()

    name = new_member_date['name']
    email = new_member_date['email']
    level = new_member_date['level']

    db.execute('update members set name = ?, email = ?, level = ? where id = ?',[name,email,level,member_id])
    db.commit()

    member_cur = db.execute('select id, name, email, level from members where id= ?',[member_id])
    new_member = member_cur.fetchone()
    
    new_member_dict = {}
    new_member_dict['id'] = new_member['id']
    new_member_dict['name'] = new_member['name']
    new_member_dict['email'] = new_member['email']
    new_member_dict['level'] = new_member['level']


    return jsonify({"member": new_member_dict})

@app.route('/member/<int:member_id>', methods=['DELETE'])
@cross_origin()
@protected
def delete_member(member_id):

    db = get_db()

    db.execute('delete from members where id=?',[member_id])
    db.commit()

    return jsonify({"message": "The member been Deleted"})

if __name__ == '__main__':
    app.run(debug=True)