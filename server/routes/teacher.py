
from flask import jsonify
from server import app
from flask import request
from server.routes.cloudantdb import *

@app.route("/teacher", methods=['GET'])
def teacher():
    usr=request.args.get('tid')
    rs = user_info(usr, "teacher")
    if rs:
        resp = {
            "data":rs, 
            "success":True
            }
    else:
        resp = {
            "data":rs, 
            "success":False,
            "error":102,
            "message": "Teacher details - Not found"
            }
    return jsonify(resp)

@app.route("/teacher_qna", methods=['GET'])
def teacher_qna():
    usr=request.args.get('tid')
    rs = get_qna(usr, "teacher")
    if rs:
        resp = {
            "data":rs, 
            "success":True
            }
    else:
        resp = {
            "data":rs, 
            "success":False,
            "error":103,
            "message": "No questions or answers for the teacher"
            }
    return jsonify(resp)

@app.route("/answer", methods=['POST'])
def answer():
    ans=request.get_json(force=True)
    rs = update_answer(ans)
    if rs:
        resp = {
            "data":rs, 
            "success":True
            }
    else:
        resp = {
            "data":rs, 
            "success":False,
            "error":105,
            "message": "Unable to update the answer in the DB"
            }
    return jsonify(resp)