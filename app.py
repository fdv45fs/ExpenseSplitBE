import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'postgresql://myuser:mypassword@localhost/ExpenseSplitV1')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(50))
    first_name = db.Column(db.String(50))

class FriendGroup(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    time_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

class Bill(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_group = db.Column(db.Integer, db.ForeignKey('friend_group.id'), nullable=False)
    description = db.Column(db.Text, nullable=False, default='')
    resolved = db.Column(db.Boolean, nullable=False, default=False)
    time_resolved = db.Column(db.DateTime)

class GroupInvitation(db.Model):
    id_group = db.Column(db.Integer, db.ForeignKey('friend_group.id'), nullable=False)
    id_account = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)
    status = db.Column(db.String(20), nullable=False)
    time_invited = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    invitation_by_id_account = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)
    __table_args__ = (db.PrimaryKeyConstraint('id_group', 'id_account', 'time_invited', 'invitation_by_id_account'),)

class Settlement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_bill = db.Column(db.Integer, db.ForeignKey('bill.id'), nullable=False)
    id_account = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)
    receiver_id_account = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    accepted = db.Column(db.Boolean, nullable=False, default=False)
    time_accepted = db.Column(db.DateTime)

class UserBelongsToGroup(db.Model):
    id_account = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)
    id_group = db.Column(db.Integer, db.ForeignKey('friend_group.id'), nullable=False)
    time_added = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    __table_args__ = (db.PrimaryKeyConstraint('id_account', 'id_group'),)

class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_bill = db.Column(db.Integer, db.ForeignKey('bill.id'), nullable=False)
    id_account = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text, nullable=False, default='')
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

class Debtor(db.Model):
    id_account = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)
    id_payment = db.Column(db.Integer, db.ForeignKey('payment.id'), nullable=False)
    amount_owed = db.Column(db.Integer, nullable=False)
    __table_args__ = (db.PrimaryKeyConstraint('id_account', 'id_payment'),)

db.create_all()

@app.route('/create_friend_group', methods=['POST'])
def create_friend_group():
    data = request.get_json()
    new_group = FriendGroup(name=data['name'])
    db.session.add(new_group)
    db.session.commit()
    return jsonify({'message': 'Friend group created successfully'})

@app.route('/add_account', methods=['POST'])
def add_account():
    data = request.get_json()
    new_account = Account(username=data['username'], password=data['password'],
                          last_name=data['last_name'], first_name=data['first_name'])
    db.session.add(new_account)
    db.session.commit()
    return jsonify({'message': 'Account added successfully'})

if __name__ == '__main__':
    app.run(debug=True)
