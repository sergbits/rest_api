import sys
from flask import Flask, request
from flask_restful import Resource, Api, reqparse, fields, marshal_with, abort
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

db = SQLAlchemy(app)
api = Api(app)

class UserModel(db.Model):
    name = db.Column(db.String(80), primary_key=True)
    pubKey = db.Column(db.String(1024), nullable=False)

    def __repr__(self):
        return f"User(name = {self.name}, pubKey = {delf.pubKey})"
    

userFields = {
    'name':fields.String,
    'pubKey':fields.String
}

@app.route('/api/db')
@marshal_with(userFields)
def user_route1():
    name = request.args.get('user', type = str)
    delete = request.args.get('delete', type = str)
    if name:
        pubKey = request.args.get('pubkey', type = str)
        if pubKey:
            user = UserModel(name=name, pubKey=pubKey)
            db.session.add(user)
            db.session.commit()
            users = UserModel.query.all()
        else:
            users = UserModel.query.filter_by(name=name).first()
            if not users:
                abort(404)
    elif delete:
        user = UserModel.query.filter_by(name=delete).first()
        if user:
            db.session.delete(user)
            db.session.commit()
        else:
            abort(404)
        users = UserModel.query.all()
    else:
        users = UserModel.query.all()

    return users, 200

@app.route('/api/pubkey')
def user_route2():
    ret = ""

    for key, value in request.args.items():
        ret += '# {0}={1}<br/>'.format(key, value)

    name = request.args.get('user', type = str)
    if name:
        users = UserModel.query.filter_by(name=name).first()
        if users:
            ret += users.pubKey

    return ret, 200


@app.route('/')
def home():
    return """
    <h1> Usage:</h1>
    <h1> &ltURL&gt/api/db?{user|delete}=&ltname&gt[&pubkey=&ltpubkey&gt]</h1>
    <h1> &ltURL&gt/api/pubkey?user=&ltname&gt</h1>
    """

if __name__ == "__main__":

    print(sys.argv.count)

    if len(sys.argv) > 1 and sys.argv[1] == "prod":
        app.run(host='0.0.0.0', port=80, debug=True)
    else:
        app.run(debug=True)
    

