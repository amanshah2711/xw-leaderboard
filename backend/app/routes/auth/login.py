from app import app

from flask import request, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from app.models import User, db
from app.utils.mail import create_and_send_verification_email
from app.utils.nyt_data import cookie_check
from app.utils.encryption import decrypt_cookie
from datetime import datetime, timezone

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()  
    email = data.get('email')
    password = data.get('password')
    user = User.query.filter_by(email=email).first()
    if user and user.check_password(password):
        if user.account_status == 'active':
            login_user(user)
            user.last_login_at = datetime.now(timezone.utc)
            db.session.commit()
            if user.encrypted_nyt_cookie and cookie_check(decrypt_cookie(user.encrypted_nyt_cookie)):
                return jsonify({"logged_in": True, "redirect" : "/daily"}), 200
            else:
                return jsonify({"logged_in": True, "redirect" : "/settings", 'message' : 'Your cookie has expired or become invalid. Please submit it again to use our service.'}), 200
        else:
            success, info = create_and_send_verification_email(email, user.id)
            if success:
                return jsonify({'logged_in' : False, 'message' : 'Email needs to be verified, a confirmation email was sent to your inbox.'})
            else:
                return jsonify({'logged_in' : False, 'message' : 'An error occurred while sending your email ' + str(info)})

        
    return jsonify({"logged_in" : False, "message":"Invalid email or password"}), 200 

@app.route('/api/logout')
@login_required
def logout():
    logout_user()
    return jsonify({"success" : False})

@app.route('/api/check-login')
def check_login():
    return jsonify({'logged_in' : bool(current_user.is_authenticated)})