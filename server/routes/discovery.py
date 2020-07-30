
from flask import jsonify
from server import app
from ibm_watson import DiscoveryV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson import ApiException
from flask import request
from server.routes.cloudantdb import *
import string

@app.route("/discover", methods=['POST'])
def discover():
    authenticator = IAMAuthenticator('m_pDdZlBFAMX8CXfCTYb0RQoh89heW0wSy-uj840d4nX')
    discovery = DiscoveryV1(
        version='2019-04-30',
        authenticator=authenticator
    )
    #version='2019-11-22
    discovery.set_service_url('https://api.eu-gb.discovery.watson.cloud.ibm.com/instances/cc6ee94e-2722-419d-b283-ac4cc5bacd91')
    discovery.set_disable_ssl_verification(True)

    try:
        #get parameters from service
        parameter = request.get_json(force=True)
        print(parameter)
        if parameter["save"]:
            teacher = get_teacher(str(parameter["sid"]), parameter["subject"].lower())
            qn={}
            qn["sid"]=str(parameter["sid"])
            qn["tid"]=teacher["teacher_id"]
            qn["question"] = parameter["question"]
            rs = add_question(qn)
            if rs:
                query_result = {"results": "You question has been sent to your teacher " + teacher["teacher_name"]}
            else:
                query_result = {"results": "Sorry, unable to send the question to your teacher. Please try later"}
        else:
            context = parameter["question"]
            query_results = discovery.query(environment_id='f186f331-22b1-4995-8b88-0d189d815cb2', collection_id='a7dde56e-64a0-4e15-842a-dcb98877167f', natural_language_query=context, passages=True, count=10).get_result()
            result=[]
            count=0
            if query_results["matching_results"]>0:
                print(query_results)
                for qr in query_results["passages"]:
                    if count < 1:
                        result.append(qr["passage_text"])
                        count += 1
                query_result={"results": result[0]}
            else:
                teacher = get_teacher(str(parameter["sid"]), parameter["subject"].lower())
                qn={}
                qn["sid"]=str(parameter["sid"])
                qn["tid"]=teacher["teacher_id"]
                qn["question"] = parameter["question"]
                rs = add_question(qn)
                if rs:
                    query_result = {"results": "You question has been sent to your teacher " + teacher["teacher_name"]}
                else:
                    query_result = {"results": "Sorry, unable to send the question to your teacher. Please try later"}
    except ApiException as ex:
        print ("Method failed with status code " + str(ex.code) + ": " + ex.message)
        query_result = {"results": "Sorry, unable to send the question to your teacher. Please try later"}
    
    return jsonify(query_result)