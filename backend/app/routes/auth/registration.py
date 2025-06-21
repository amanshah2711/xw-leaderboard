from app import app
from flask import request, jsonify, redirect
from app.models import db, User
from app.utils.social import generate_link
from app.utils.encryption import generate_token, verify_token
from app.utils import frontend_url
from app.utils.mail import send_email_verification_email
from app.forms.auth import RegistrationForm
from datetime import datetime, timezone


@app.route('/api/register', methods=['POST'])
def register():
    form = RegistrationForm()
    if form.validate():
        data = request.get_json()

        username = data.get('username')
        email = data.get('email')
        password = data.get('password')

        invite_link = generate_link()

        if User.query.filter_by(email=email).first():
            return jsonify({"success": False, "message": "Email is already registered"}), 200
        user = User(username=username, email=email, invite_link=invite_link)
        user.set_password(password)

        db.session.add(user)
        db.session.commit()

        token = generate_token(email, 'verify-email-salt')
        verify_url = frontend_url + '/api/verify-email/' + token
        send_email_verification_email(verify_url, email) # Add a try catch to redirect if email fails or add option to resend

        return jsonify({"success": True, "message": "Log In To Your Account"}), 200
    else:
        message = ''
        for field, errors in form.errors.items():
            for error in errors:
                print(f"Error in {field}: {error}")
                message += f'Error in {field}: {error}' + '\n \n'
        return jsonify({"success": False, "message": message}), 200

@app.route('/api/verify-email/<token>')
def verify_email(token):
    email = verify_token(token=token, salt='verify-email-salt', expiration=3600)
    if not email:
        return jsonify({'success' : False, 'message':'Password reset link appears to be invalid. Make a new request to reset your password.'}), 200
    else:
        user = User.query.filter_by(email=email).first()
        if user:
            user.email_verified = True
            user.email_verified_at = datetime.now(timezone.utc)
            user.account_status = 'active'
            db.session.commit()
            return redirect(frontend_url + "?message=Email%20Verified%20Successfully") 
        else:
            return redirect(frontend_url + "?message=Error%20Occurred") 

