
from flask import request, jsonify
from flask_login import login_user, login_required, logout_user
from app import app
from .models import User, db


@app.route('/api/login', methods=['POST' ])
def login():
    if request.method == 'POST':
        data = request.get_json()  # This retrieves the JSON data sent in the body
        username = data.get('email')  # Your React app sends 'email', so adjust accordingly
        password = data.get('password')
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            return jsonify({"message": "Login Successful", "user": user.username, "success": True}), 200
        return jsonify({"message":"Invalid username or password"}), 401 

@app.route('/api/register', methods=['POST'])
def register():
    pass

@app.route('/api/add_friend', methods=['POST'])
def add_friend():
    pass

@app.route('/api/remove_friend', methods=['POST'])
def remove_friend():
    pass

@app.route('/api/friends', methods=['POST'])
def friends():
    pass