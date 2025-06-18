from app import app
from flask import request, jsonify
from app.models import db, User
from app.utils.social import generate_link
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

        return jsonify({"success": True, "message": "Log In To Your Account"}), 200
    else:
        message = ''
        for field, errors in form.errors.items():
            for error in errors:
                print(f"Error in {field}: {error}")
                message += f'Error in {field}: {error}' + '\n \n'
        return jsonify({"success": False, "message": message}), 200

@app.route('/api/verify_email/<token>', methods=['POST'])
def verify_email():
    pass
