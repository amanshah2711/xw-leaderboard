from app import app
from flask import request, jsonify
from flask_login import login_required, current_user
from app.models import db 
from app.utils.encryption import decrypt_cookie, encrypt_cookie
from app.utils.nyt_data import NYTRequestError, nyt_request, nyt_puzzle_metadata
from datetime import datetime
from zoneinfo import ZoneInfo
@app.route('/api/auth/nyt/store-cookie', methods=['POST'])
@login_required
def store_cookie(): 
    data = request.get_json()  
    cookie = 'NYT-S=' + data.get('nytCookie')
    try:
        current_user.encrypted_nyt_cookie = encrypt_cookie(cookie)
        nyt_request(nyt_puzzle_metadata(datetime.now(tz=ZoneInfo('America/New_York')).date().isoformat()), current_user)
        db.session.commit()
        return jsonify({'success': True, "message": "Your cookie has been safely stored"}), 200
    except NYTRequestError as e:
        return jsonify({'success': False, "message": "Your cookie was invalid please make sure it was entered correctly, or try again later(NYT may be down)"}), 200


@app.route('/api/auth/nyt/remove-cookie', methods=['POST'])
@login_required
def remove_cookie(): 
    current_user.invalidate_nyt_cookie()
    return jsonify({"success": True, "message": "Your cookie has been deleted and your NYT account disconnected"}), 200

@app.route('/api/auth/nyt/valid-cookie', methods=['GET'])
@login_required
def valid_cookie(): 
    if current_user.encrypted_nyt_cookie:
        return jsonify({'success' : True, 'message' : '', 'is_valid' : True}), 200
    else:
        return jsonify({'success' : True, 'message' : '', 'is_valid' : False}), 200