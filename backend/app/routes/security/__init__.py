from app import app

from flask import jsonify, make_response
from flask_wtf.csrf import generate_csrf

@app.route("/api/csrf-token", methods=["GET"])
def get_csrf():
    response = make_response(jsonify({"csrf_token": generate_csrf()}))
    return response