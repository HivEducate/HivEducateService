
from flask import jsonify
from server import app
from flask import request
from server.routes.cloudantdb import *

@app.route("/student", methods=['GET'])
def student():
    usr=request.args.get('sid')
    rs = user_info(usr, "student")
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
            "message": "Student details - Not found"
            }
    return jsonify(resp)

@app.route("/student_qna", methods=['GET'])
def student_qna():
    usr=request.args.get('sid')
    rs = get_qna(usr, "student")
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
            "message": "No questions or answers for the student"
            }
    return jsonify(resp)

@app.route("/view", methods=['POST'])
def view():
    vw=request.get_json(force=True)
    rs = update_view(vw)
    if rs:
        resp = {
            "data":rs, 
            "success":True
            }
    else:
        resp = {
            "data":rs, 
            "success":False,
            "error":106,
            "message": "Unable to update the view status in the DB"
            }
    return jsonify(resp)

@app.route("/question", methods=['POST'])
def question():
    qn=request.get_json(force=True)
    rs = add_question(qn)
    if rs:
        resp = {
            "data":rs, 
            "success":True
            }
    else:
        resp = {
            "data":rs, 
            "success":False,
            "error":107,
            "message": "Unable to add the question in the DB"
            }
    return jsonify(resp)

@app.route("/qn_by_subject", methods=['POST'])
def qn_by_subject():
    parameter=request.get_json(force=True)
    teacher = get_teacher(parameter["sid"], parameter["subject"])
    qn={}
    qn["sid"]=parameter["sid"]
    qn["tid"]=teacher["teacher_id"]
    qn["question"] = parameter["question"]
    rs = add_question(qn)
    if rs:
        resp = {
            "data":rs, 
            "success":True
            }
    else:
        resp = {
            "data":rs, 
            "success":False,
            "error":107,
            "message": "Unable to add the question in the DB"
            }
    return jsonify(resp)