from app import app

from flask import request, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from app.models import User, db
from app.utils.mail import create_and_send_verification_email
from app.utils.nyt_data import commit_or_raise
from datetime import datetime, timezone

import logging
logger = logging.getLogger(__name__)

@app.post('/api/auth/login')
def login():
    data = request.get_json()  
    email = data.get('email')
    password = data.get('password')
    user = User.query.filter_by(email=email).first()
    if not user or not user.check_password(password):
        logger.info('Failed login of user with email: ' + str(email) + '. Either email or password is incorrect.')
        return jsonify({"logged_in" : False, "message":"Invalid email or password"}), 200 
    elif user.account_status == 'active':
        login_user(user)
        user.last_login_at = datetime.now(timezone.utc)
        commit_or_raise()
        logger.info('Successful login of user with email: ' + str(email))
        if user.encrypted_nyt_cookie:
            return jsonify({"logged_in": True, "redirect" : "/nyt-daily"}), 200
        else:
            return jsonify({"logged_in": True, "redirect" : "/nyt-settings", 'message' : 'Your cookie has expired or become invalid. Please submit it again to use our service.'}), 200
    else:
        logger.info('Failed login of user with email: ' + str(email) + '. Account is not active current status is ' + str(user.account_status))
        success, info = create_and_send_verification_email(email, user.id)
        if success:
            return jsonify({'logged_in' : False, 'message' : 'Email needs to be verified, a confirmation email was sent to your inbox.'})
        else:
            return jsonify({'logged_in' : False, 'message' : 'An error occurred while sending your email'}) 

@app.route('/api/auth/logout')
@login_required
def logout():
    logout_user()
    return jsonify({"success" : False})

@app.route('/api/auth/check-login')
def check_login():
    return jsonify({'logged_in' : bool(current_user.is_authenticated)}), 200