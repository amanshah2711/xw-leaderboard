
import requests
import app
from flask import jsonify
import datetime as dt
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo
import time
from .encryption import decrypt_cookie
from ..models import db, CrosswordData
from sqlalchemy.dialects.postgresql import insert

# Define the New York time zone
new_york_tz = ZoneInfo("America/New_York")

# Get the current date and time in New York
now_in_new_york = datetime.now(new_york_tz)

# Format the date as YYYY-MM-DD
formatted_date = now_in_new_york.strftime('%Y-%m-%d')

# Archive start date
#archive_start_date = datetime(1993, 11, 21, tzinfo=new_york_tz).date()
archive_start_date = datetime(2025, 1, 1, tzinfo=new_york_tz).date()
#mini_start_date = datetime(2014, 8, 21, tzinfo=new_york_tz).date()
mini_start_date = datetime(2025, 1, 1, tzinfo=new_york_tz).date()

bonus_start_date = datetime(1997, 2, 1, tzinfo=new_york_tz).date()

# NYT API Base (links below figured out by monitoring network traffic)
nyt_base_url = 'https://www.nytimes.com'

# backend endpoints
backend_endpoint = 'svc/crosswords/v6'

metadata_endpoint = 'puzzle/daily'
history_endpoint = lambda date_start, date_end : f'svc/crosswords/v3/puzzles.json?publish_type=daily&sort_order=asc&sort_by=print_date&date_start={date_start}&date_end={date_end}'

mini_metadata_endpoint = 'puzzle/mini'
mini_history_endpoint = lambda date_start, date_end : f'svc/crosswords/v3/puzzles.json?publish_type=mini&sort_order=asc&sort_by=print_date&date_start={date_start}&date_end={date_end}'

bonus_metadata_endpoint = 'puzzle/bonus'
bonus_history_endpoint = lambda date_start, date_end : f'svc/crosswords/v3/puzzles.json?publish_type=bonus&sort_order=asc&sort_by=print_date&date_start={date_start}&date_end={date_end}'

data_endpoint = 'game'

#frontend endpoints
puzzle_endpoint = 'crosswords/game/daily'
mini_puzzle_endpoint = 'crosswords/game/mini'
bonus_puzzle_endpoint = 'crosswords/game/bonus'

# NYT Puzzle Link (Add date in YYYY/MM/DD to end of link; note different with puzzle endpoint)
nyt_puzzle_url = lambda date_string: f'{nyt_base_url}/{puzzle_endpoint}/{date_string}'

# NYT Puzzle Endpoint (Add date in YYYY-MM-DD.json to the end)
nyt_puzzle_metadata = lambda date_string : f'{nyt_base_url}/{backend_endpoint}/{metadata_endpoint}/{date_string}.json'

# NYT Puzzle Data (Add gameid.json to the end)
nyt_puzzle_solve_data = lambda game_id : f'{nyt_base_url}/{backend_endpoint}/{data_endpoint}/{game_id}.json'

#NYT Mini Puzzle Link (Add data in YYYY/MM/DD to the end of link)
nyt_mini_puzzle_url = lambda date_string: f'{nyt_base_url}/{mini_puzzle_endpoint}/{date_string}'

#NYT Mini Puzzle Endpoint (Add date in YYYY-MM-DD.json to the end)
nyt_mini_puzzle_metadata = lambda date_string : f'{nyt_base_url}/{backend_endpoint}/{mini_metadata_endpoint}/{date_string}.json'

#NYT Mini Puzzle Data
nyt_mini_puzzle_solve_data = lambda game_id : f'{nyt_base_url}/{backend_endpoint}/{data_endpoint}/{game_id}.json'

# NYT Puzzle Link (Add date in YYYY/MM to end of link; note different with puzzle endpoint)
nyt_bonus_puzzle_url = lambda date_string: f'{nyt_base_url}/{bonus_puzzle_endpoint}/{date_string}'

# NYT Puzzle Endpoint (Add date in YYYY-MM-DD.json to the end)
nyt_bonus_puzzle_metadata = lambda date_string : f'{nyt_base_url}/{backend_endpoint}/{bonus_metadata_endpoint}/{date_string}.json'

# NYT Puzzle Data (Add gameid.json to the end)
nyt_bonus_puzzle_solve_data = lambda game_id : f'{nyt_base_url}/{backend_endpoint}/{data_endpoint}/{game_id}.json'

create_header = lambda cookie : {'Cookie' : cookie, 'User-Agent' : 'XWLeaderboard/1.0'}

def valid_puzzle_date(date, variant):
    datetime_in_new_york = datetime.now(tz=ZoneInfo('America/New_York'))
    upper_bound = datetime_in_new_york.date()
    if datetime_in_new_york.weekday() in range(5) \
            and dt.time(22, 0, 0, tzinfo=ZoneInfo('America/New_York')) <= datetime_in_new_york.time():
        upper_bound += timedelta(days=1)
    if datetime_in_new_york.weekday() in [5,6] and dt.time(18, 0, 0, tzinfo=ZoneInfo('America/New_York')) <= datetime_in_new_york.time():
        upper_bound += timedelta(days=1)
    if variant == 'daily':
        return archive_start_date <= date and date <= upper_bound 
    elif variant == 'mini':
        return mini_start_date <= date and date <= upper_bound 
    elif variant == 'bonus':
        return bonus_start_date <= date and date.day == 1 and date <= upper_bound #TODO: VERIFY UPPERBOUND THING WORKS
    else:
        return False

class NYTRequestError(Exception):
    pass

def nyt_request(url, user, session=None):
    if not user.encrypted_nyt_cookie:
        raise NYTRequestError('User has no submitted cookie')
    cookie = decrypt_cookie(user.encrypted_nyt_cookie)
    headers = create_header(cookie=cookie)

    requester = session if session else requests

    for attempt in range(3):
        try:
            response = requester.get(url, headers=headers, timeout=5)
            if response.status_code in [401, 403]:
                user.invalidate_nyt_cookie()
                raise NYTRequestError('Invalid NYT Cookie')
            elif response.status_code >= 500:
                time.sleep(0.5 * (attempt + 1))
                continue
            elif response.status_code == 200:
                return response.json()
               
            else:
                raise NYTRequestError(f'request failed with status {response.status_code}')
        except requests.exceptions.RequestException as e:
            if attempt == 2:
                raise NYTRequestError(f"Request failed: {e}")
            time.sleep(0.3 * (attempt + 1))

    raise NYTRequestError('No successful connection')

def get_puzzle_metadata(date_string, user, variant = 'daily', session=None): 
    if variant == 'daily':
        metadata = nyt_puzzle_metadata
    elif variant == 'mini':
        metadata = nyt_mini_puzzle_metadata
    else:
        metadata = nyt_bonus_puzzle_metadata
    return nyt_request(metadata(date_string), user, session=session)
    
def get_puzzle_statistics_by_date(date_string, user, variant = 'daily', session=None):
    if variant == 'daily':
        solve_data = nyt_puzzle_solve_data
    elif variant == 'mini':
        solve_data = nyt_mini_puzzle_solve_data
    else:
        solve_data = nyt_bonus_puzzle_solve_data
    puzzle_info = get_puzzle_metadata(date_string, user, variant, session)
    puzzle_id = puzzle_info['id']
    return nyt_request(solve_data(puzzle_id), user, session)

def get_puzzle_statistics_by_puzzle_id(puzzle_id, user, variant = 'daily', session=None):
    if variant == 'daily':
        solve_data = nyt_puzzle_solve_data
    elif variant == 'mini':
        solve_data = nyt_mini_puzzle_solve_data
    else:
        solve_data = nyt_bonus_puzzle_solve_data
    return nyt_request(solve_data(puzzle_id), user, session)

def upsert(user, date, status, solve_time, percent_filled, variant='daily'):
    entry = CrosswordData.query.filter(CrosswordData.user_id == user.id, CrosswordData.date == date, CrosswordData.source == 'nyt', CrosswordData.variant == variant).first()
    utc_now = datetime.now(timezone.utc)
    if entry:
        entry.status, entry.solve_time, entry.last_fetched = status, solve_time, utc_now 
    else:
        stmt = insert(CrosswordData).values(user_id=user.id, date=date, solve_time=solve_time, status=status, percent_filled=percent_filled, source='nyt', variant=variant, last_fetched=utc_now).on_conflict_do_nothing(index_elements=['user_id', 'date','source', 'variant'])
        db.session.execute(stmt)
    return status, solve_time

def fupsert_by_date(user, date, variant='daily', refresh=False, session=None):
    entry = CrosswordData.query.filter(CrosswordData.user_id == user.id, CrosswordData.date == date, CrosswordData.source == 'nyt', CrosswordData.variant == variant).first()
    current_date = datetime.now(new_york_tz).date()

    crossword_complete = entry and entry.status == 'complete'

    refresh_required = not crossword_complete or \
        (not crossword_complete and abs(date - current_date) <= timedelta(weeks=2)) or \
        (not crossword_complete and abs(entry.last_fetched - current_date) > timedelta(days=1))
    
    if refresh or refresh_required:
        puzzle_statistics = get_puzzle_statistics_by_date(date.isoformat(), user, variant, session)
        if 'solved' in puzzle_statistics['calcs'] and puzzle_statistics['calcs']['solved']: # Check for reset solves right now it appears "firsts" appears. Check does open, solved equate to solve time or other way to interpolate solve time
            solve_time = puzzle_statistics['calcs']['secondsSpentSolving']
            return upsert(user, date, 'complete', solve_time, 100, variant=variant)
        elif 'percentFilled' in puzzle_statistics['calcs']:
            return upsert(user, date, 'partial', None, puzzle_statistics['calcs']['percentFilled'], variant=variant)
        else:
            return upsert(user, date, 'unattempted', None, 0, variant=variant)
    else:
        return entry.status, entry.solve_time

def aggregrate_solved_puzzles(user, variant='daily'):
    upper_bound = datetime.now(new_york_tz).date()
    lower_bound = upper_bound - timedelta(days=90)
    if variant == 'daily':
        history_url = history_endpoint 
        start_date = archive_start_date
    elif variant == 'mini':
        history_url = mini_history_endpoint
        start_date = mini_start_date
    else:
        history_url = bonus_history_endpoint
        start_date = bonus_start_date

    results = []
    with requests.Session() as session:
        while (lower_bound >= start_date and upper_bound >= lower_bound): 
            response = nyt_request(nyt_base_url + '/' + history_url(lower_bound.strftime('%Y-%m-%d'), upper_bound.strftime('%Y-%m-%d')), user, session=session)
            upper_bound = lower_bound - timedelta(days=1)
            lower_bound = max(upper_bound - timedelta(days=90), start_date)
            results += response['results']
            time.sleep(0.5)
        return results
