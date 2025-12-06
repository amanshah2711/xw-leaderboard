from app import app
from flask import request, jsonify, redirect
from app.models import db, User
from app.utils.social import generate_link
from app.utils.encryption import generate_token, verify_token
from app.utils import frontend_url
from app.utils.encryption import password_reset_salt, email_verify_salt
from app.utils.mail import create_and_send_verification_email 
from app.forms.auth import RegistrationForm
from datetime import datetime, timezone


@app.post('/api/auth/register')
def register():
    form = RegistrationForm()
    if form.validate():
        data = request.get_json()
        try:
            display_name = data.get('displayName')
            email = data.get('email')
            password = data.get('password')

            invite_link = generate_link()

            if User.query.filter_by(email=email).first():
                return jsonify({"success": False, "message": "Email is already registered"}), 200
            user = User(display_name=display_name, email=email, invite_link=invite_link)
            user.set_password(password)
            success, info = create_and_send_verification_email(email, user.id)
            if success:
                db.session.add(user)
                db.session.commit()
                return jsonify({"success": True, "message": "Verify your email and log in."}), 200
            else:
                return jsonify({"success": False, "message": "We had an issue processing your email."}), 200
        except Exception as e:
            return jsonify({"success": False, "message": "We had an issue processing your email."}), 200 
    else:
        message = ''
        for field, errors in form.errors.items():
            for error in errors:
                print(f"Error in {field}: {error}")
                message += f'Error in {field}: {error}' + '\n \n'
        return jsonify({"success": False, "message": message}), 200


