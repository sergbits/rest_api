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

@app.route('/api/pubkey')
@marshal_with(userFields)
def user_route():
    name = request.args.get('name', type = str)
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

@app.route('/')
def home():
    return '<h1> Usage: &ltURL&gt/api/pubkey?{name|delete}=&ltname&gt[&pubkey=&ltpubkey&gt]</h1>'

if __name__ == "__main__":
    app.run(debug=True)

