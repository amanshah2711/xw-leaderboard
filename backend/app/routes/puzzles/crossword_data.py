from app import app
from flask import Response
from flask_login import login_required, current_user
from app.models import CrosswordData

import csv
import io

@app.get('/api/puzzles/nyt/<nyt_variant:variant>/puzzle-history', defaults={'source': 'nyt'})
@login_required
def export_data(source, variant):
    output = io.StringIO()
    writer = csv.writer(output)

    # Write header row
    writer.writerow(['Date', 'Puzzle Source', 'Puzzle Variant', 'Solve Time(s)', 'Status', 'Percent Filled', 'Last Fetched'])

    # Query user's data
    data = CrosswordData.query.filter_by(user_id=current_user.id, source=source, variant=variant).order_by(CrosswordData.date).all()

    for entry in data:
        writer.writerow([
            entry.date.strftime('%Y-%m-%d'),
            entry.source,
            entry.variant,
            entry.solve_time,
            entry.status,
            entry.percent_filled,
            entry.last_fetched.isoformat() if entry.last_fetched else ''
        ])

    # Create response with correct headers
    output.seek(0)
    return Response(
        output,
        mimetype='text/csv',
        headers={'Content-Disposition': f'attachment; filename={entry.source}_{entry.variant}_crossword_data.csv'}
    )