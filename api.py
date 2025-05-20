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
    if name:
        pubKey = request.args.get('pubKey', type = str)
        if pubKey:
            user = UserModel(name=name, pubKey=pubKey)
            db.session.add(user)
            db.session.commit()
            users = user
        else:
            users = UserModel.query.filter_by(name=name).first()
            if not users:
                abort(404)
    else:
        users = UserModel.query.all()

    return users, 200

@app.route('/')
def home():
    return '<h1> Database access: /api/user?name=&ltname&gt[&pubKey=&ltpubKey&gt]</h1>'

if __name__ == "__main__":
    app.run(debug=True)

