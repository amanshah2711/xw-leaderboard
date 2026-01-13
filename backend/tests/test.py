from app import app 
from app.models import User
from app.utils.nyt_data import aggregrate_solved_puzzles

def test_aggregate_bonus_puzzles():
    with app.app_context():
        user = User.query.filter(User.email == 'amanshah2711@gmail.com').first()
        assert user is not None, "User not found"
        
        result = aggregrate_solved_puzzles(user, 'bonus')
        for d in result:
            print(d['print_date'])

if __name__ == "__main__":
    test_aggregate_bonus_puzzles()