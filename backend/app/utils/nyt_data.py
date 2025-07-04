
import requests
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo
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
archive_start_date = datetime(2024, 9, 21, tzinfo=new_york_tz)

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
        stmt = insert(CrosswordData).values(user_id=user.id, day=date, solve_time=solve_time, status=status, percent_filled=percent_filled, kind=kind, last_fetched=utc_now).on_conflict_do_nothing(index_elements=['user_id', 'day'])
        db.session.execute(stmt)

def fupsert(user, date, kind='daily'):
    puzzle_statistics = get_puzzle_statistics(date, decrypt_cookie(user.encrypted_nyt_cookie), type=kind)
    if 'solved' in puzzle_statistics['calcs'] and puzzle_statistics['calcs']['solved']: # Check for reset solves right now it appears "firsts" appears. Check does open, solved equate to solve time or other way to interpolate solve time
        solve_time = puzzle_statistics['calcs']['secondsSpentSolving']
        upsert(user, date, 'complete', solve_time, 100, kind=kind)
    elif 'percentFilled' in puzzle_statistics['calcs']:
        upsert(user, date, 'partial', None, puzzle_statistics['calcs']['percentFilled'], kind=kind)
    else:
        upsert(user, date, 'unattempted', None, 0, kind=kind)

def aggregrate_solved_puzzles(cookie, type='daily'):
    upper_bound = now_in_new_york
    lower_bound = now_in_new_york - timedelta(days=90)
    history_url = history_endpoint if type == 'daily' else mini_history_endpoint
    results = []
    while (lower_bound >= archive_start_date and upper_bound >= lower_bound): 
        response = requests.get(nyt_base_url + '/' + history_url(lower_bound.strftime('%Y-%m-%d'), upper_bound.strftime('%Y-%m-%d')), headers=create_header(cookie))
        if response.json() and response.json()['status'] == 'OK':
            upper_bound = lower_bound - timedelta(days=1)
            lower_bound = max(upper_bound - timedelta(days=90), archive_start_date)
            results += response.json()['results']
        else:
            print('Error occurred while fetching data')
            return
    return results

def get_puzzle_info(date_string, cookie, type='daily'): 
    metadata = nyt_puzzle_metadata if type == 'daily' else nyt_mini_puzzle_metadata
    response = requests.get(metadata(date_string), headers=create_header(cookie))
    if response.status_code == 200:
        return response.json()
    else:
        print('Error while fetching metadata')

def get_puzzle_statistics(date_string, cookie, type='daily'):
    puzzle_info = get_puzzle_info(date_string, cookie, type=type)
    solve_data = nyt_puzzle_solve_data if type == 'daily' else nyt_mini_puzzle_solve_data
    if puzzle_info:
        response = requests.get(solve_data(puzzle_info['id']), headers=create_header(cookie))
        if response.status_code == 200:
            return response.json()
        else:
            print('Error while fetching puzzle times')
 
def cookie_check(cookie): #NYT response returns a json with key "message" and value "Forbidden" for invalid cookies
    return bool(get_puzzle_info(formatted_date, cookie))