from app import app
from flask import request, jsonify
from app.models import db, User
from app.utils.social import generate_link
from app.utils.encryption import generate_token, verify_token
from app.utils import frontend_url
from app.utils.mail import send_email_verification_email
from app.forms.auth import RegistrationForm


@app.route('/api/register', methods=['POST'])
def register():
    form = RegistrationForm()
    if form.validate():
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

        token = generate_token(email, 'verify-email-salt')
        verify_url = frontend_url + '/verify-email/' + token
        send_email_verification_email(verify_url, email) # Add a try catch to redirect if email fails or add option to resend

        return jsonify({"success": True, "message": "Log In To Your Account"}), 200
    else:
        message = ''
        for field, errors in form.errors.items():
            for error in errors:
                print(f"Error in {field}: {error}")
                message += f'Error in {field}: {error}' + '\n \n'
        return jsonify({"success": False, "message": message}), 200

@app.route('/api/verify-email/<token>', methods=['POST'])
def verify_email(token):
    email = verify_token(token=token, salt='verify-email-salt', expiration=3600)
    if not email:
        return jsonify({'success' : False, 'message':'Password reset link appears to be invalid. Make a new request to reset your password.'}), 200
    else:
        pass
