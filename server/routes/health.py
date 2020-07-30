
from flask import jsonify
from server import app
from server.routes.cloudantdb import *

@app.route("/health")
def health():
    """health route"""
    state = {"status": "UP"}
    return QnADAO().list()
