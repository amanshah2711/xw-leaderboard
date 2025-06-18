
import requests
from datetime import datetime
from zoneinfo import ZoneInfo

# Define the New York time zone
new_york_tz = ZoneInfo("America/New_York")

# Get the current date and time in New York
now_in_new_york = datetime.now(new_york_tz)

# Format the date as YYYY-MM-DD
formatted_date = now_in_new_york.strftime('%Y-%m-%d')

# NYT API Base (figured out by monitoring network traffic)
nyt_base_url = 'https://www.nytimes.com'

# backend endpoints
backend_endpoint = 'svc/crosswords/v6'
metadata_endpoint = 'puzzle/daily'
mini_metadata_endpoint = 'puzzle/mini'
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