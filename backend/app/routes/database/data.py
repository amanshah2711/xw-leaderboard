
from app import app
from flask_login import login_required, current_user


@app.route('nyt-data-export/<kind>')
@login_required
def export(kind):
    pass