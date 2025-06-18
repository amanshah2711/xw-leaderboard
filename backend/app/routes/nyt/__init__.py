from app import app
from flask import request, jsonify
from flask_login import login_required, current_user
from app.models import User, CrosswordData, Friends, db
from app.utils.nyt_data import get_puzzle_statistics, nyt_mini_puzzle_url, nyt_puzzle_url, cookie_check
from app.utils.encryption import decrypt_cookie, encrypt_cookie
from sqlalchemy.dialects.postgresql import insert

from datetime import datetime

@app.route('/api/sync/<date_string>/<kind>', methods=['GET'])
@login_required
def sync(date_string, kind):
    target_date = datetime.strptime(date_string, '%Y-%m-%d').date()

    friends = db.session.query(Friends).filter(Friends.friend_one == current_user.id).all()
    group_ids = set([friend.friend_two for friend in friends] + [current_user.id])

    completed_data_query = db.session.query(CrosswordData).filter(CrosswordData.user_id.in_(group_ids), CrosswordData.day == target_date, CrosswordData.status == 'complete', CrosswordData.kind == kind).order_by(CrosswordData.solve_time.asc()).all()
    completed_data = [{'username' : User.query.filter_by(id=data.user_id).first().username, 'solve_time': data.solve_time} for data in completed_data_query]
    completed_ids = set([data.user_id for data in completed_data_query])
    
    ids_to_check = group_ids - completed_ids
    for id in ids_to_check:
        user = User.query.filter_by(id=id).first()
        if user.encrypted_nyt_cookie: # Make sure to check and validate cookies
            puzzle_statistics = get_puzzle_statistics(date_string, decrypt_cookie(user.encrypted_nyt_cookie), type=kind)
            if 'solved' in puzzle_statistics['calcs'] and puzzle_statistics['calcs']['solved']: # Check for reset solves right now it appears "firsts" appears. Check does open, solved equate to solve time or other way to interpolate solve time
                entry = db.session.query(CrosswordData).filter(CrosswordData.user_id == id, CrosswordData.day == target_date, CrosswordData.kind == kind).first()
                solve_time = puzzle_statistics['calcs']['secondsSpentSolving']
                if entry:
                    entry.status, entry.solve_time = 'complete', solve_time
                else:
                    stmt = insert(CrosswordData).values(user_id=id, day=target_date, solve_time=solve_time, status='complete', kind=kind).on_conflict_do_nothing(index_elements=['user_id', 'day'])
                    db.session.execute(stmt)

                completed_data.append({'username' : user.username, 'solve_time': solve_time})
                completed_ids.add(id)

    db.session.commit()

    incompleted_ids = group_ids - completed_ids
    incompleted_data = [User.query.filter_by(id=id).first().username for id in incompleted_ids]

    completed_data.sort(key=lambda d:d['solve_time'])
    
    return jsonify({"complete" : completed_data, "incomplete" : incompleted_data}), 200

@app.route('/api/puzzle-link/<date_string>/<kind>', methods=['GET'])
@login_required
def get_puzzle_link(date_string, kind):
    puzzle_url = nyt_puzzle_url if kind == 'daily' else nyt_mini_puzzle_url
    if request.method == 'GET':
        target_date = datetime.strptime(date_string, '%Y-%m-%d').strftime('%Y/%m/%d')
        return jsonify({'puzzle_link' : puzzle_url(target_date)})

@app.route('/api/store-cookie', methods=['POST'])
@login_required
def store_cookie(): #Add validation verificatoin and updating of cookies
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