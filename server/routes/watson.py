
from flask import jsonify
from server import app
from ibm_watson import AssistantV2
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson import ApiException
from flask import request

@app.route("/myhealth")
def myhealth():
    """health route"""
    state = {"status": "UPS"}
    return jsonify(state)

@app.route("/sendmessage")
def sendmessage():
	txt=request.args.get('txt')
	
	apikey='vBOIg92dGqhTTgU3fA2W1zLsjughb7R18g5z24ULcjfi'
	version1='2020-04-01'
	url='https://api.eu-gb.assistant.watson.cloud.ibm.com/instances/afd39c9f-8f90-4ff7-9047-5c86c564c732'
	assistant_id = '99418e38-b023-41a2-bf43-050acb1bab85'
	
	# authenticate watson
	authenticator = IAMAuthenticator(apikey)
	assistant = AssistantV2(version=version1,authenticator=authenticator)

	assistant.set_service_url(url)
	
	try:
		response = assistant.message_stateless(
			assistant_id=assistant_id,
    		input={
    			'message_type': 'text',
        		'text': txt
    		}
		).get_result()
	
	except ApiException as ex:
   		print ("Method failed with status code " + str(ex.code) + ": " + ex.message)
	
	txtResponse = "Sorry, i could not help you at this time"
	if response['output']['generic']:
		if response['output']['generic'][0]['response_type'] == 'text':
			txtResponse = response['output']['generic'][0]['text']
	
	return jsonify(txtResponse)
