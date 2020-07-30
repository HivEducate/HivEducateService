
from flask import jsonify
from server import app
from flask import request
from server.routes.cloudantdb import *

@app.route("/login", methods=['GET'])
def login():
    usr=request.args.get('usr')
    rs = check_user(usr)
    if rs:
        resp = {
            "data":rs, 
            "success":True
            }
    else:
        resp = {
            "data":rs, 
            "success":False,
            "error":101,
            "message": "No such user"
            }
    return jsonify(resp)