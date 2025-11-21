from app import app
from flask import request, jsonify, Response
from flask_login import login_required, current_user
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from app.models import User, CrosswordData, Friends, db
from app.utils.nyt_data import get_puzzle_statistics, nyt_mini_puzzle_url, nyt_puzzle_url, cookie_check, aggregrate_solved_puzzles, upsert, fupsert, new_york_tz
from app.utils.encryption import decrypt_cookie, encrypt_cookie
from sqlalchemy.dialects.postgresql import insert

import time
import requests
from threading import Thread

from datetime import datetime, timedelta

import csv
import io

limiter = Limiter(get_remote_address, app=app)

@app.errorhandler(429)
def ratelimit_handler(e):
    return jsonify({
        "error": "Too many requests",
        "message": "You've hit the sync limit. Try again in 24 hours."
    }), 429


def sync_all(kind, user):
    with app.app_context():
        results = aggregrate_solved_puzzles(decrypt_cookie(user.encrypted_nyt_cookie), type=kind) 
        session = requests.Session()
        for day in results:
            target_date = datetime.strptime(day['print_date'], '%Y-%m-%d').date()
            if day['solved']:
                status = 'complete'
                fupsert(user, target_date, kind=kind, session=session, id=day['puzzle_id'])
                time.sleep(0.5)
            elif day['percent_filled']:
                status = 'partial'
                solve_time = None
                upsert(user, target_date, status, solve_time, day['percent_filled'], kind=kind)
            else:
                status = 'unattempted'
                solve_time = None
                upsert(user, target_date, status, solve_time, 0, kind=kind)
        db.session.commit()


@app.route('/api/full-sync/<kind>', methods=['GET', 'POST'])
@limiter.limit('2 per day')
@login_required
def async_all(kind):
    Thread(target=sync_all, args=(kind, current_user._get_current_object())).start()
    return jsonify({'message' : f'Sync for {kind} crosswords has started. This may take some time if you have many solves.\n'})


@app.route('/api/sync/<date_string>/<kind>/<force>', methods=['GET'])
@login_required
def sync(date_string, kind, force):
    target_date = datetime.strptime(date_string, '%Y-%m-%d').date()
    force= force == 'True'

    friends = db.session.query(Friends).filter(Friends.friend_one == current_user.id).all()
    group_ids = set([friend.friend_two for friend in friends] + [current_user.id])

    completed_data_query = db.session.query(CrosswordData).filter(CrosswordData.user_id.in_(group_ids), CrosswordData.day == target_date, CrosswordData.status == 'complete', CrosswordData.kind == kind).order_by(CrosswordData.solve_time.asc()).all()
    completed_data = [{'username' : User.query.filter_by(id=data.user_id).first().username, 'solve_time': data.solve_time, 'id' : data.user_id} for data in completed_data_query]
    completed_ids = set([data.user_id for data in completed_data_query])

    ids_to_check = group_ids - completed_ids
    for id in ids_to_check:
        user = User.query.filter_by(id=id).first()
        if user.encrypted_nyt_cookie and cookie_check(decrypt_cookie(user.encrypted_nyt_cookie)): # Make sure to check and validate cookies
            status, solve_time = fupsert(user, target_date, kind, force=force)
            if status == 'complete':
                completed_data.append({'username' : user.username, 'solve_time': solve_time, 'id': id})
                completed_ids.add(id)

    db.session.commit()

    incompleted_ids = group_ids - completed_ids
    incompleted_data = [{'username' : User.query.filter_by(id=id).first().username, 'id' : id} for id in incompleted_ids]

    completed_data.sort(key=lambda d:d['solve_time'])
    
    return jsonify({"complete" : completed_data, "incomplete" : incompleted_data, 'current_user' : current_user.id}), 200

@app.route('/api/export-data/<kind>', methods=['GET', 'POST'])
@login_required
def export_data(kind):
    output = io.StringIO()
    writer = csv.writer(output)

    # Write header row
    writer.writerow(['Date', 'Kind', 'Solve Time (s)', 'Status', 'Percent Filled', 'Last Fetched'])

    # Query user's data
    data = CrosswordData.query.filter_by(user_id=current_user.id, kind=kind).order_by(CrosswordData.day).all()

    for entry in data:
        writer.writerow([
            entry.day.strftime('%Y-%m-%d'),
            entry.kind,
            entry.solve_time,
            entry.status,
            entry.percent_filled,
            entry.last_fetched.strftime('%Y-%m-%d') if entry.last_fetched else ''
        ])

    # Create response with correct headers
    output.seek(0)
    return Response(
        output,
        mimetype='text/csv',
        headers={'Content-Disposition': f'attachment; filename={kind}_crossword_data.csv'}
    )

@app.route('/api/puzzle-link/<date_string>/<kind>', methods=['GET'])
@login_required
def get_puzzle_link(date_string, kind):
    puzzle_url = nyt_puzzle_url if kind == 'daily' else nyt_mini_puzzle_url
    if request.method == 'GET':
        target_date = datetime.strptime(date_string, '%Y-%m-%d').strftime('%Y/%m/%d')
        return jsonify({'puzzle_link' : puzzle_url(target_date)})
