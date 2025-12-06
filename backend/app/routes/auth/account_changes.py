from app import app

from flask import request, jsonify, redirect
from flask_login import login_required, current_user
from app.models import User, CrosswordData, Friendship, db
from app.utils.mail import send_reset_email, create_and_send_verification_email, email_verify_salt
from app.utils.social import valid_display_name
from app.utils.encryption import generate_token, verify_token, password_reset_salt
from app.utils import frontend_url
from app.forms.auth import PasswordChangeForm
from datetime import datetime, timezone

@app.post('/api/auth/change-password')
@login_required
def change_password():
    form = PasswordChangeForm()
    if form.validate():
        data = request.get_json()  
        password = data.get('password')
        current_user.set_password(password) 
        db.session.commit()
        return jsonify({'success': True, 'message': 'Your password has been successfully changed'}), 200
    else:
        message = ''
        for field, errors in form.errors.items():
            for error in errors:
                print(f"Error in {field}: {error}")
                message += f'Error in {field}: {error}' + '\n \n'
        return jsonify({"success": False, "message": message}), 200

@app.post('/api/auth/change-email')
@login_required
def change_email():
    data = request.get_json()  
    email = data.get('email')
    user = User.query.filter_by(email=email).first()
    if not user:
        success, info = create_and_send_verification_email(email, current_user.id)
        if success:
            return jsonify({'success': True, 'message': 'We attempted to send an email to ' + email + '. Check your inbox, it may take a few minutes.'}), 200
        else:
            return jsonify({'success': False, 'message': 'We had an issue processing your email. Try again later.' + email}), 200
    else:
        if current_user.email == email:
            message = 'Your account already uses this email'
        else:
            message = 'This email is in use with a different account'
        return jsonify({'success': True, 'message': message}), 200

@app.post('/api/auth/change-display-name')
@login_required
def change_display_name():
    data = request.get_json()  
    new_display_name = data.get('displayName')
    if valid_display_name(new_display_name):
        current_user.display_name = new_display_name 
        message = 'Your display name has been successfully changed. Visit the leaderboard to see it!'
        db.session.commit()
    else:
        message = 'Our profanity filter has not approved of your new display name.'

    return jsonify({'success': True, 'message' : message}), 200

@app.post('/api/auth/request-reset-password')
def request_reset_password():
    data = request.get_json()
    email = data.get('email')
    token = generate_token(email, password_reset_salt)
    reset_url = frontend_url + '/reset-password/' + token

    success, info = send_reset_email(reset_url, email)
    if success:
        return jsonify({'success': True, 'message': 'Succesfully sent link to your email, if it exists.', 'debug': reset_url, 'info': info}), 200
    else:
        return jsonify({'success': False, 'message': 'There was an error sending you an email. Make sure your email was properly entered.', 'debug': reset_url, 'info': info}), 200

@app.post('/api/auth/reset-password/<token>')
def reset_password(token):
    email = verify_token(token=token, salt=password_reset_salt, expiration=3600)
    if not email:
        return jsonify({'success' : False, 'message':'Password reset link appears to be invalid. Make a new request to reset your password.'}), 200
    
    form = PasswordChangeForm()
    if form.validate():
        data = request.get_json()
        user = User.query.filter_by(email=email).first()
        new_password = data.get('password')
        user.set_password(new_password)
        db.session.commit()
        return jsonify({'success' : False, 'message' : 'Password successfully changed'}), 200
    else:
        message = ''
        for field, errors in form.errors.items():
            for error in errors:
                print(f"Error in {field}: {error}")
                message += f'Error in {field}: {error}' + '\n \n'
        return jsonify({"success": False, "message": message}), 200

@app.route('/api/auth/verify-email/<token>')
def verify_email(token):
    data = verify_token(token=token, salt=email_verify_salt, expiration=3600)
    if not data:
        return jsonify({'success' : False, 'message':data}), 200
    else:
        user = User.query.filter_by(id=data['id']).first()
        if user:
            user.email = data['addressee']
            user.email_verified = True
            user.email_verified_at = datetime.now(timezone.utc)
            user.account_status = 'active'
            db.session.commit()
            return redirect(frontend_url + "?message=Email%20Verified%20Successfully") 
        else:
            return redirect(frontend_url + "?message=Error%20Occurred") 

@app.post('/api/auth/delete-account')
@login_required
def delete_account():
    user = current_user
    CrosswordData.query.filter_by(user_id=user.id).delete(synchronize_session=False)
    Friendship.query.filter((Friendship.node_one == user.id) | (Friendship.node_two == user.id)).delete(synchronize_session=False)
    db.session.delete(user)
    db.session.commit()
    return jsonify({'success': True}), 200