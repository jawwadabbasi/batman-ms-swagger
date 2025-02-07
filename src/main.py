# Built with ingenuity,
# by Jawwad Abbasi (jawwad@kodelle.com)

# Initiates a Flask app to handle managed endpoints
# and relays to corresponding controller and module
# for processing.

import json
import settings

from flask import Flask,Response,request
from flasgger import Swagger
from v1.controller import Ctrl_v1
from v2.controller import Ctrl_v2
from v1.docify import Docify

app = Flask(__name__)
swagger = Swagger(app, template=Docify.SwaggerApiYaml())

@app.errorhandler(404)
def RouteNotFound(e):
    return Response(None, status=400, mimetype='application/json')

####################################
# Supported endpoints for API v1
####################################
@app.route('/api/v1/Api/CreateLog', methods=['POST'])
def ApiLog():
    data = Ctrl_v1.ApiLog(request.args)
    return Response(json.dumps(data), status=data['ApiHttpResponse'], mimetype='application/json')

####################################
# Initiate web server
####################################
app.run(host='0.0.0.0', port=settings.FLASK_PORT, debug=settings.FLASK_DEBUG)