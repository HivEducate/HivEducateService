
from cloudant.client import Cloudant
from cloudant.error import CloudantException
from cloudant.result import Result
from flask import jsonify
from datetime import date
import time


# IAM Authentication (uncomment if needed, and comment out previous IBM Cloudant Legacy authentication section)
client = Cloudant.iam("e96bbea2-7d6b-4a35-b6ed-affbd38d101c-bluemix", "cJbLX3IZqBiw6exOClY1rwC6Qn8NHpVfIAuxFGv6G5zU")
client.connect()

#check user
def check_user(usr):
    db = client["user"]
    result = []
    usr_data = db.get_query_result(selector={'_id': {'$eq': usr}})
    for user in usr_data:
        result = user
    return result

#get teacher/student info
def user_info(usr, role):
    if role=="teacher":
        db = client["teacher"]
    elif role=="student":
        db = client["student"]
    result =[]
    usr_data = db.get_query_result(selector={'_id': {'$eq': usr}})
    for user in usr_data:
        result = user
    return result

#get qna by teacher / student
def get_qna(usr, role):
    db = client["question_answer"]
    result =[]
    if role=="teacher":
        qna_data = db.get_query_result(selector={"answered_by": {'teacher_id': {'$eq': usr}}})
    elif role=="student":
        qna_data = db.get_query_result(selector={"asked_by": {'student_id': {'$eq': usr}}})
    for qna in qna_data:
        result.append(qna)
    return result
    
#update answer to the document
def update_answer(answer):
    teacher = user_info(answer["tid"], "teacher")
    result = []
    try:
        db = client["question_answer"]
        document = db[answer["_id"]]
        doc_exists = answer["_id"] in db
        if doc_exists:
            document["answered"] = True
            document["answer"] = answer["answer"]
            document["answered_date"] = str(date.today())
            document["answered_by"]["teacher_id"] = answer["tid"]
            document["answered_by"]["teacher_name"] = teacher["name"]
            document.save()
            result=[{"_id": answer["_id"]}]
    except Exception as e:
        print(e)
    return result

#update viewed status in the document
def update_view(view):
    result = []
    try:
        db = client["question_answer"]
        document = db[view["_id"]]
        doc_exists = view["_id"] in db
        if doc_exists:
            document["viewed"] = True
            document["viewed_date"] = str(date.today())
            document.save()
            result=[{"_id": view["_id"]}]
    except Exception as e:
        print(e)
    return result

#Add the question into DB
def add_question(qn):
    result = []
    try:
        student = user_info(qn["sid"], "student")
        time.sleep(1)
        teacher = user_info(qn["tid"], "teacher")
        time.sleep(1)
        db = client["question_answer"]
        question = {
            "question": qn["question"],
            "answer": "",
            "answered": False,
            "answered_date": "",
            "asked_by": {
                "student_id": qn["sid"],
                "student_name": student["name"]
                },
            "asked_date": str(date.today()),
            "answered_by": {
                "teacher_id": qn["tid"],
                "teacher_name": teacher["name"]
                },
            "viewed": False,
            "viewed_date": ""
            }
        document = db.create_document(question)
        if document.exists():
            result=[{"_id": document["_id"]}]
            print(result)
    except Exception as e:
        print(e)
    return result

#get teacher info from student info and subject
def get_teacher(sid, sub):
    student = user_info(sid, "student")
    time.sleep(1)
    db = client["class"]
    result =[]
    cls_data = db.get_query_result(selector={'_id': {'$eq': student["studying"]}})
    for clss in cls_data:
        for teacher in clss["teacher"]:
            if teacher["primary_subject"] == sub:
                result = teacher
    return result