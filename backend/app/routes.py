
from flask import request, jsonify
from flask_login import login_user, login_required, logout_user
from app import app
from .models import User, db


@app.route('/api/login', methods=['POST' ])
def login():
    if request.method == 'POST':
        data = request.get_json()  
        email = data.get('email')
        password = data.get('password')
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            login_user(user)
            return jsonify({"message": "Login Successful", "success": True}), 200
        return jsonify({"message":"Invalid username or password", "success" : False}), 401 

@app.route('/api/register', methods=['POST'])
def register():
    if request.method == 'POST':
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        if User.query.filter_by(email=email).first():
            return jsonify({"message": "Email is already registered"}), 400

        user = User(email=email)
        user.set_password(password)

        db.session.add(user)
        db.session.commit()

        login_user(user)

        return jsonify({"user": user.email, "success": False, "registration" : False, "message" : "Log In With Your New Account"}), 200


@app.route('/api/add_friend', methods=['POST'])
def add_friend():
    if request.method == 'POST':
        data = request.json()

@app.route('/api/remove_friend', methods=['POST'])
def remove_friend():
    if request.method == 'POST':
        data = request.json()

@app.route('/api/friends', methods=['POST'])
def friends():
    if request.method == 'POST':
        data = request.json()