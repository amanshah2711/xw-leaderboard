from app import app
from flask import request, jsonify
from flask_login import login_required, current_user
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from app.models import CrosswordData, db
from app.utils.nyt_data import nyt_bonus_puzzle_url,nyt_mini_puzzle_url, nyt_puzzle_url, aggregrate_solved_puzzles, upsert, valid_puzzle_date, fupsert_by_date, NYTRequestError
from app.utils.nyt_data import commit_or_raise

import time
import requests
from threading import Thread

from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
import logging
logger = logging.getLogger(__name__)


@app.get('/api/puzzles/nyt/<nyt_variant:variant>/latest/date')
@login_required
def get_latest_puzzle(variant):
    if variant == 'daily' or variant == 'mini':
        date = datetime.now(tz=ZoneInfo('America/New_York')).date()
    elif variant == 'bonus':
        date = datetime.now(tz=ZoneInfo('America/New_York')).date().replace(day=1)
    return jsonify({'date':date.isoformat()}) 

@app.get('/api/puzzles/nyt/<nyt_variant:variant>/<date_string>/puzzle-link')
@login_required
def get_puzzle_link(date_string, variant):
    if variant == 'daily':
        puzzle_url = nyt_puzzle_url
    elif variant == 'mini':
        puzzle_url = nyt_mini_puzzle_url
    else:
        puzzle_url = nyt_bonus_puzzle_url
    target_date = datetime.strptime(date_string, '%Y-%m-%d').strftime('%Y/%m/%d')
    return jsonify({'puzzle_link' : puzzle_url(target_date)})

@app.get('/api/puzzles/nyt/<nyt_variant:variant>/<date_string>/metadata')
def get_puzzle_metadata(date_string, variant):
    date = datetime.strptime(date_string, '%Y-%m-%d').date()
    if variant == 'mini' or variant == 'daily':
        if valid_puzzle_date(date=date, variant=variant):
            next_date = date + timedelta(days=1)
            prev_date = date + timedelta(days=-1)
            next_date = next_date if valid_puzzle_date(date=next_date, variant=variant) else date
            prev_date = prev_date if valid_puzzle_date(date=prev_date, variant=variant) else date
            return jsonify({'exists' : True, 'date' : date.isoformat(), 'next_date' : next_date.isoformat(), 'prev_date' : prev_date.isoformat()})
        else:
            return jsonify({'exists' : False})
    if variant == 'bonus':
        if valid_puzzle_date(date=date, variant=variant):
            if date.month in range(2, 12):
                next_date = date.replace(month = date.month + 1)
                prev_date = date.replace(month = date.month - 1)
            elif date.month == 1:
                next_date = date.replace(month = date.month + 1)
                prev_date = date.replace(month = 12).replace(year=date.year-1)
            elif date.month == 12:
                next_date = date.replace(month = 1).replace(year=date.year+1)
                prev_date = date.replace(month = date.month - 1)
            if prev_date == datetime(1998, 9, 1).date():
                prev_date = datetime(1998, 8, 1).date()
            next_date = next_date if valid_puzzle_date(date=next_date, variant=variant) else date
            prev_date = prev_date if valid_puzzle_date(date=prev_date, variant=variant) else date
            return jsonify({'exists' : True, 'date' : date.isoformat(), 'next_date' : next_date.isoformat(), 'prev_date' : prev_date.isoformat()})
        else:
            return jsonify({'exists' : False})


@app.get('/api/puzzles/nyt/<nyt_variant:variant>/<date_string>/rankings')
@login_required
def get_puzzle_rankings(date_string, variant):
    target_date = datetime.strptime(date_string, '%Y-%m-%d').date()
    refresh = request.args.get("refresh", "false").lower() == "true"

    id_to_user = {user.id:user for user in current_user.get_friends()}
    id_to_user[current_user.id] = current_user
    group_ids = id_to_user.keys()

    completed_puzzle_rows = CrosswordData.query.filter(CrosswordData.user_id.in_(group_ids), CrosswordData.date == target_date, CrosswordData.status == 'complete', CrosswordData.source == 'nyt', CrosswordData.variant == variant).all()
    completed_puzzle_data = [{
            'display_name' : id_to_user[row.user_id].display_name, 
            'solve_time': row.solve_time, 
            'id' : row.user_id
        } for row in completed_puzzle_rows]
    completed_puzzle_user_ids = set([data['id'] for data in completed_puzzle_data])

    ids_to_check = group_ids - completed_puzzle_user_ids
    for id in ids_to_check:
        user = id_to_user[id]
        if user.encrypted_nyt_cookie:
            try:
                status, solve_time = fupsert_by_date(user, date=target_date, variant=variant, refresh=refresh, session=None)
            except NYTRequestError as e:
                logger.info('A request to the NYT has failed when trying to query the following date' + str(target_date)) 
            else:
                if status == 'complete':
                    completed_puzzle_data.append({'display_name' : user.display_name, 'solve_time': solve_time, 'id': id})
                    completed_puzzle_user_ids.add(id)

    commit_or_raise()

    incompleted_ids = group_ids - completed_puzzle_user_ids
    incompleted_data = [{'display_name' : id_to_user[id].display_name, 'id' : id} for id in incompleted_ids]

    completed_puzzle_data.sort(key=lambda d:d['solve_time'])
    
    return jsonify({"complete" : completed_puzzle_data, "incomplete" : incompleted_data, 'current_user' : current_user.id}), 200


limiter = Limiter(get_remote_address, app=app)
@app.errorhandler(429)
def ratelimit_handler(e):
    return jsonify({
        "error": "Too many requests",
        "message": "You've hit the sync limit. Try again in 24 hours."
    }), 429


def sync_all(variant, user):
    with app.app_context():
        results = aggregrate_solved_puzzles(user=user, variant=variant) 
        with requests.Session() as session:
            for date in results:
                target_date = datetime.strptime(date['print_date'], '%Y-%m-%d').date()
                if date['solved']:
                    status = 'complete'
                    fupsert_by_date(user, target_date, variant=variant, session=session)
                    time.sleep(0.5)
                elif date['percent_filled']:
                    status = 'partial'
                    solve_time = None
                    upsert(user, target_date, status, solve_time, date['percent_filled'], variant=variant)
                else:
                    status = 'unattempted'
                    solve_time = None
                    upsert(user, target_date, status, solve_time, 0, variant=variant)
            commit_or_raise()


@app.post('/api/puzzles/nyt/<nyt_variant:variant>/sync-all')
@limiter.limit('3 per day')
@login_required
def async_all(variant):
    Thread(target=sync_all, args=(variant, current_user._get_current_object())).start()
    return jsonify({'message' : f'Sync for NYT {variant} crosswords has started. This may take some time if you have many solves.\n'})