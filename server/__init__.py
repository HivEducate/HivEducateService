import os
from flask import Flask, abort, session, request, redirect
from flask.json import jsonify
from flask_cors import CORS

app = Flask(__name__, template_folder="../public", static_folder="../public", static_url_path='')
CORS(app)

from server.routes import *
from server.services import *

initServices(app)

if 'FLASK_LIVE_RELOAD' in os.environ and os.environ['FLASK_LIVE_RELOAD'] == 'true':
	import livereload
	app.debug = True
	server = livereload.Server(app.wsgi_app)
	server.serve(port=os.environ['port'], host=os.environ['host'])
