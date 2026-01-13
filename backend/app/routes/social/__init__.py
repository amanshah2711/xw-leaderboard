from app import app
from flask import request, jsonify, redirect
from flask_login import login_required, current_user
from app.models import User, Friendship, db
from app.utils.social import invite_formatter, generate_link
from app.utils.nyt_data import commit_or_raise
import datetime


@app.get('/api/social/get-invite')
@login_required
def get_invite_link():
    return jsonify({'success' : True, "invite" : invite_formatter(current_user.invite_link)}) 

@app.get('/api/social/invite/<invite_token>')
@login_required
def process_invite(invite_token):
    user = User.query.filter_by(invite_link=invite_token).first()
    if user:
        current_user.add_friend(user)
        return redirect('/', code=302)
    else:
        return "Invite invalid", 404

@app.post('/api/social/reset-invite')
@login_required
def reset_invite_link():
    current_user.invite_link = generate_link()
    commit_or_raise()
    return jsonify({'success' : True, "invite" : invite_formatter(current_user.invite_link)}), 200

@app.post('/api/social/remove-friend')
@login_required
def remove_friend():
    data = request.get_json()
    friend_id = data.get('friend_id')
    current_user.remove_friend(User.query.filter_by(id=friend_id).first())
    return jsonify({'message': 'Friendship successfully deleted. Refresh to see updated leaderboard.'}), 200