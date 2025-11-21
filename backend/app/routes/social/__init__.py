from app import app
from flask import request, jsonify, redirect
from flask_login import login_required, current_user
from app.models import User, Friendship, db
from app.utils.social import invite_formatter, generate_link
import datetime


@app.route('/api/get-invite', methods=['GET'])
@login_required
def get_invite_link():
    if request.method == 'GET':
        return jsonify({'success' : True, "invite" : invite_formatter(current_user.invite_link)}) 


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

@app.route('/api/reset-invite', methods=['POST'])
@login_required
def reset_invite_link():
    current_user.invite_link = generate_link()
    db.session.commit()
    return jsonify({'success' : True, "invite" : invite_formatter(current_user.invite_link)}), 200

@app.route('/api/remove-friend', methods=['POST'])
@login_required
def remove_friend():
    if request.method == 'POST':
        data = request.get_json()
        id_a = data.get('friend_one')
        id_b = data.get('friend_two')
        friend_entry = Friends.query.filter_by(friend_one = id_a, friend_two = id_b).first()
        friend_entry2 = Friends.query.filter_by(friend_one = id_b, friend_two = id_a).first()
        if friend_entry:
            db.session.delete(friend_entry)
            db.session.delete(friend_entry2)
            db.session.commit()
            return jsonify({'message': 'Friendship successfully deleted. Refresh to see updated leaderboard.'}), 200
        else:
            return jsonify({'message': 'An error occurred while deleting your friend'}), 200