from app import app

from flask import request, jsonify
from flask_login import login_required, current_user
from app.models import User, CrosswordData, Friends, db
from app.utils.mail import send_reset_email
from app.utils.encryption import generate_token, verify_token
from app.utils import frontend_url
from app.forms.auth import PasswordChangeForm

@app.route('/api/change-password', methods=['POST'])
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

@app.route('/api/change-email', methods=['POST'])
@login_required
def change_email():
    data = request.get_json()  
    email = data.get('email')
    user = User.query.filter_by(email=email).first()
    if not user:
        current_user.email = email 
        db.session.commit()
        return jsonify({'success': True, 'message': 'Your email has been successfully changed to ' + email}), 200
    else:
        if current_user.email == email:
            message = 'Your account already uses this email'
        else:
            message = 'This email is in use with a different account'
        return jsonify({'success': True, 'message': message}), 200

@app.route('/api/change-username', methods=['POST'])
@login_required
def change_username():
    data = request.get_json()  
    new_username = data.get('username')
    current_user.username = new_username
    db.session.commit()
    return jsonify({'success': True, 'message' : 'Your username has been successfully changed. Visit the leaderboard to see it!'}), 200

@app.route('/api/request-reset-password', methods=['POST'])
def request_reset_password():
    data = request.get_json()
    email = data.get('email')
    token = generate_token(email, 'password-reset-salt')
    reset_url = frontend_url + '/reset-password/' + token

    send_reset_email(reset_url, email)
    
    return jsonify({'success': True, 'message': 'Succesfully sent link to your email, if it exists.', 'debug': reset_url}), 200

@app.route('/api/reset-password/<token>', methods=['POST'])
def reset_password(token):
    email = verify_token(token=token, salt='password-reset-salt', expiration=3600)
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

@app.route('/api/delete-account', methods=['POST'])
@login_required
def delete_account():
    user = current_user
    CrosswordData.query.filter_by(user_id=user.id).delete(synchronize_session=False)
    Friends.query.filter((Friends.friend_one == user.id) | (Friends.friend_two == user.id)).delete(synchronize_session=False)
    db.session.delete(user)
    db.session.commit()
    return jsonify({'success': True}), 200