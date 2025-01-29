
from flask import request, jsonify, redirect
from flask_login import login_user, login_required, current_user, logout_user
import namer
from app import app
from .models import User, db, Friends, CrosswordData
from datetime import datetime
from .utils import encrypt_cookie, decrypt_cookie, get_puzzle_statistics, cookie_check
import os

generate_link = lambda : namer.generate(category="scientists", suffix_length=4)
invite_formatter = lambda code : "/api/invite/" + code
frontend_url = os.getenv('FRONTEND_URL', 'http://localhost:5173')

@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data.get('email')
    username = data.get('username')
    password = data.get('password')
    invite_link = generate_link()
    if User.query.filter_by(email=email).first():
        return jsonify({"success": False, "message": "Email is already registered"}), 200

    user = User(email=email, username=username, invite_link=invite_link)
    user.set_password(password)

    db.session.add(user)
    db.session.commit()

    login_user(user)

    return jsonify({"success": True, "message": "Log In To Your Account"}), 200

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()  
    email = data.get('email')
    password = data.get('password')
    user = User.query.filter_by(email=email).first()
    if user and user.check_password(password):
        login_user(user)
        if user.encrypted_nyt_cookie and cookie_check(decrypt_cookie(user.encrypted_nyt_cookie)):
            return jsonify({"logged_in": True, "redirect" : "/leaderboard"}), 200
        else:
            return jsonify({"logged_in": True, "redirect" : "/cookies"}), 200
    return jsonify({"logged_in" : False, "message":"Invalid username or password"}), 200 

@app.route('/api/logout')
@login_required
def logout():
    logout_user()
    return jsonify({"success" : False})

@app.route('/api/check_login')
def check_login():
    if current_user.is_authenticated:
        return jsonify({"logged_in": True})
    else:
        return jsonify({"logged_in": False})
    
@app.route('/api/sync/<date_string>', methods=['GET'])
@login_required
def sync(date_string):
    target_date = datetime.strptime(date_string, '%Y-%m-%d').date()

    friends = db.session.query(Friends).filter(Friends.friend_one == current_user.id).all()
    group_ids = set([friend.friend_two for friend in friends] + [current_user.id])

    completed_data_query = db.session.query(CrosswordData).filter(CrosswordData.user_id.in_(group_ids), CrosswordData.day == target_date, CrosswordData.status == 'complete').order_by(CrosswordData.solve_time.asc()).all()
    completed_data = [{'username' : User.query.filter_by(id=data.user_id).first().username, 'solve_time': data.solve_time} for data in completed_data_query]
    completed_ids = set([data.user_id for data in completed_data_query])
    
    ids_to_check = group_ids - completed_ids
    for id in ids_to_check:
        user = User.query.filter_by(id=id).first()
        if user.encrypted_nyt_cookie: # Make sure to check and validate cookies
            puzzle_statistics = get_puzzle_statistics(date_string, decrypt_cookie(user.encrypted_nyt_cookie))
            if 'solved' in puzzle_statistics['calcs'] and puzzle_statistics['calcs']['solved']: # Check for reset solves right now it appears "firsts" appears. Check does open, solved equate to solve time or other way to interpolate solve time
                entry = db.session.query(CrosswordData).filter(CrosswordData.user_id == id, CrosswordData.day == target_date).with_for_update().first()
                if entry:
                    entry.status, entry.solve_time = 'complete', puzzle_statistics['calcs']['secondsSpentSolving']
                else:
                    entry = CrosswordData(user_id=id, day=target_date, solve_time=puzzle_statistics['calcs']['secondsSpentSolving'], status='complete')
                    db.session.add(entry)
                completed_data.append({'username' : user.username, 'solve_time': entry.solve_time})
                completed_ids.add(id)

    db.session.commit()

    incompleted_ids = group_ids - completed_ids
    incompleted_data = [User.query.filter_by(id=id).first().username for id in incompleted_ids]

    completed_data.sort(key=lambda d:d['solve_time'])
    
    return jsonify({"complete" : completed_data, "incomplete" : incompleted_data}), 200

@app.route('/api/get_invite', methods=['GET'])
@login_required
def get_invite_link():
    if request.method == 'GET':
        return jsonify({"invite" : invite_formatter(current_user.invite_link)}) 

@app.route('/api/invite/<invite_token>', methods=['GET'])
def process_invite(invite_token):
    user = User.query.filter_by(invite_link=invite_token).first()
    if user:
        if current_user.is_authenticated and current_user != user and not db.session.query(Friends).filter(Friends.friend_one == current_user.id, Friends.friend_two == user.id).first(): #Add check for friendship already existing
            new_friendship1 = Friends(friend_one=user.id, friend_two=current_user.id)
            new_friendship2 = Friends(friend_one=current_user.id, friend_two=user.id)
            db.session.add(new_friendship1)
            db.session.add(new_friendship2)
            db.session.commit()
            return redirect('/', code=302)
        else:
            return redirect('/', code=302)
    else:
        return "Invite invalid", 404

@app.route('/api/day_rankings', methods=['GET'])
def rankings():
    return jsonify({"message": "You have successfully added a friend!"}), 200

@app.route('/api/reset_invite', methods=['POST'])
def reset_invite_link():
    user = User.query.get(current_user.id)
    if user:
        user.invite_link = generate_link()
        db.session.commit()
        return jsonify({"invite" : invite_formatter(user.invite_link)}), 200

@app.route('/api/remove_friend', methods=['POST'])
@login_required
def remove_friend():
    if request.method == 'POST':
        data = request.json()

@app.route('/api/store_cookie', methods=['POST'])
@login_required
def store_cookie(): #Add validation verificatoin and updating of cookies
    data = request.get_json()  
    cookie = data.get('nytCookie')
    if cookie_check(cookie):
        encrypted_cookie = encrypt_cookie(cookie)
        current_user.encrypted_nyt_cookie = encrypted_cookie
        db.session.commit()
        return jsonify({"message": "Your cookie has been safely stored"}), 200
    else:
        return jsonify({"message": "The submitted cookie was invalid"}), 400

@app.route('/api/remove_cookie', methods=['POST'])
@login_required
def remove_cookie(): 
    current_user.encrypted_nyt_cookie = None
    db.session.commit()
    return jsonify({"message": "Your cookie has been deleted and your NYT account disconnected"}), 200

@app.route('/api/valid_cookie', methods=['GET'])
@login_required
def valid_cookie(): 
    return jsonify(bool(current_user.encrypted_nyt_cookie)), 200
