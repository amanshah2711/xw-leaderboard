from app import app
from flask import request, jsonify
from flask_login import login_required, current_user
from .. import db 
from app.utils.nyt_data import cookie_check
from app.utils.encryption import decrypt_cookie, encrypt_cookie

@app.route('/api/store-cookie', methods=['POST'])
@login_required
def store_cookie(): 
    data = request.get_json()  
    cookie = 'NYT-S=' + data.get('nytCookie')
    if cookie_check(cookie):
        encrypted_cookie = encrypt_cookie(cookie)
        current_user.encrypted_nyt_cookie = encrypted_cookie
        db.session.commit()
        return jsonify({'success': True, "message": "Your cookie has been safely stored"}), 200
    else:
        return jsonify({'success': False, "message": "The submitted cookie was invalid"}), 200 

@app.route('/api/remove-cookie', methods=['POST'])
@login_required
def remove_cookie(): 
    current_user.encrypted_nyt_cookie = None
    db.session.commit()
    return jsonify({"success": True, "message": "Your cookie has been deleted and your NYT account disconnected"}), 200

@app.route('/api/valid-cookie', methods=['GET'])
@login_required
def valid_cookie(): 
    if current_user.encrypted_nyt_cookie:
        return jsonify({'success' : True, 'message' : '', 'is_valid' : cookie_check(decrypt_cookie(current_user.encrypted_nyt_cookie))}), 200
    else:
        return jsonify({'success' : True, 'message' : '', 'is_valid' : False}), 200