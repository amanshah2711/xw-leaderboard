
import requests
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
archive_start_date = datetime(1993, 11, 21, tzinfo=new_york_tz).date()
mini_start_date = datetime(2014, 8, 21, tzinfo=new_york_tz).date()

# NYT API Base (figured out by monitoring network traffic)
nyt_base_url = 'https://www.nytimes.com'

# backend endpoints
backend_endpoint = 'svc/crosswords/v6'
metadata_endpoint = 'puzzle/daily'
history_endpoint = lambda date_start, date_end : f'svc/crosswords/v3/puzzles.json?publish_type=daily&sort_order=asc&sort_by=print_date&date_start={date_start}&date_end={date_end}'

mini_metadata_endpoint = 'puzzle/mini'
# This doesn't work TODO: debug
mini_history_endpoint = lambda date_start, date_end : f'svc/crosswords/v3/puzzles.json?publish_type=mini&sort_order=asc&sort_by=print_date&date_start={date_start}&date_end={date_end}'

data_endpoint = 'game'

#frontend endpoints
puzzle_endpoint = 'crosswords/game/daily'
mini_puzzle_endpoint = 'crosswords/game/mini'

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

create_header = lambda cookie : {'Cookie' : cookie, 'User-Agent' : 'XWLeaderboard/1.0'}

def upsert(user, date, status, solve_time, percent_filled, kind='daily'):
    entry = db.session.query(CrosswordData).filter(CrosswordData.user_id == user.id, CrosswordData.day == date, CrosswordData.kind == kind).first()
    utc_now = datetime.now(timezone.utc)
    if entry:
        entry.status, entry.solve_time, entry.last_fetched = status, solve_time, utc_now 
    else:
        stmt = insert(CrosswordData).values(user_id=user.id, day=date, solve_time=solve_time, status=status, percent_filled=percent_filled, kind=kind, last_fetched=utc_now).on_conflict_do_nothing(index_elements=['user_id', 'day', 'kind'])
        db.session.execute(stmt)
    return status, solve_time

def fupsert(user, date, kind='daily', force=False, session=None, id=None):
    entry = db.session.query(CrosswordData).filter(CrosswordData.user_id == user.id, CrosswordData.day == date, CrosswordData.kind == kind).first()
    current_date = datetime.now(new_york_tz).date()
    is_there_data = entry and entry.status == 'complete'
    does_data_needs_refresh = not entry or (not is_there_data and abs(date - current_date) <= timedelta(weeks=2)) or (not is_there_data and abs(entry.last_fetched - current_date) > timedelta(days=1))
    if force or does_data_needs_refresh:
        puzzle_statistics = get_puzzle_statistics(date, decrypt_cookie(user.encrypted_nyt_cookie), type=kind, session=session, id=id)
        if 'solved' in puzzle_statistics['calcs'] and puzzle_statistics['calcs']['solved']: # Check for reset solves right now it appears "firsts" appears. Check does open, solved equate to solve time or other way to interpolate solve time
            solve_time = puzzle_statistics['calcs']['secondsSpentSolving']
            return upsert(user, date, 'complete', solve_time, 100, kind=kind)
        elif 'percentFilled' in puzzle_statistics['calcs']:
            return upsert(user, date, 'partial', None, puzzle_statistics['calcs']['percentFilled'], kind=kind)
        else:
            return upsert(user, date, 'unattempted', None, 0, kind=kind)
    else:
        return entry.status, entry.solve_time


def aggregrate_solved_puzzles(cookie, type='daily'):
    session = requests.Session()
    upper_bound = datetime.now(new_york_tz).date()
    lower_bound = upper_bound - timedelta(days=90)
    history_url = history_endpoint if type == 'daily' else mini_history_endpoint
    results = []
    count = 0
    start_date = archive_start_date if type == 'daily' else mini_start_date
    while (lower_bound >= start_date and upper_bound >= lower_bound): 
        response = session.get(nyt_base_url + '/' + history_url(lower_bound.strftime('%Y-%m-%d'), upper_bound.strftime('%Y-%m-%d')), headers=create_header(cookie))
        print('iteration count: ', count)
        count += 1
        if response.json() and response.json()['status'] == 'OK':
            upper_bound = lower_bound - timedelta(days=1)
            lower_bound = max(upper_bound - timedelta(days=90), archive_start_date)
            results += response.json()['results']
            time.sleep(0.5)
        else:
            print('Error occurred while fetching data')
            return
    return results

def get_puzzle_info(date_string, cookie, type='daily', session=None): 
    metadata = nyt_puzzle_metadata if type == 'daily' else nyt_mini_puzzle_metadata
    try:
        if session:
            response = session.get(metadata(date_string), headers=create_header(cookie))
        else:
            response = requests.get(metadata(date_string), headers=create_header(cookie))
        print('status code:', response.status_code, date_string, cookie, flush=True)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Failed request: {response.status_code} {response.reason}", flush=True)
    except Exception as e:
        print('Request failed:', e)
        return None

def get_puzzle_statistics(date_string, cookie, type='daily', id=None, session=None):
    if not id:
        puzzle_info = get_puzzle_info(date_string, cookie, type=type)
        id = puzzle_info['id']
    solve_data = nyt_puzzle_solve_data if type == 'daily' else nyt_mini_puzzle_solve_data
    if session:
        response = session.get(solve_data(id), headers=create_header(cookie))
    else:
        response = requests.get(solve_data(id), headers=create_header(cookie))
    if response.status_code == 200:
        return response.json()
    else:
        print('Error while fetching puzzle times')
 
def cookie_check(cookie): #NYT response returns a json with key "message" and value "Forbidden" for invalid cookies
    return bool(get_puzzle_info(formatted_date, cookie))
